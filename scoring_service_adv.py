import grpc
import json
import logging
from log_utils import *
from concurrent import futures
import scoring_pb2, scoring_pb2_grpc

ACCURACY_WEIGHT = 1.4

class ScoringService(scoring_pb2_grpc.ScoringServiceServicer):
    def __init__(self):
        with open("leaderboard.json", "r") as f:
            self.leaderboard = json.load(f)

    @LogCalls(name=__name__)
    def SubmitResult(self, request, context):

        accuracy = float(calc_accuracy(request.typed_text, request.prompt))
        speed = float(calc_speed(request.typed_text, request.duration))
        score = float(calc_score(accuracy, speed))

        entry = {"name": request.name, "level": request.level, "accuracy": accuracy, "speed": speed, "score": score}
        #entry = scoring_pb2.LeaderboardEntry(name=request.name, level=request.level, accuracy=accuracy, speed=speed, score=score)
        
        self.leaderboard[str(request.level)].append(entry)

        self.leaderboard[str(request.level)] = sorted(self.leaderboard[str(request.level)], key=lambda entry: entry["score"], reverse=True)[:3]
        
        with open("leaderboard.json", "w") as f:
            json.dump(self.leaderboard, f)

        return scoring_pb2.ScoreResponse(accuracy=accuracy, speed=speed, score=score)

    @LogCalls(name=__name__)
    def GetLeaderboard(self, request, context):
        
        #print(self.leaderboard, type(self.leaderboard))

        parsed_leaderboard = {"1":[], "2":[], "3":[]}

        #print(parsed_leaderboard)

        for level, scores in self.leaderboard.items():
            #print(level, scores)
            for score in scores:
                #print(score)
                score_entry = scoring_pb2.LeaderboardEntry(name=score["name"], level=score["level"], accuracy=score["accuracy"], speed=score["speed"], score=score["score"])
                parsed_leaderboard[level].append(score_entry)

        #print(parsed_leaderboard)

        return scoring_pb2.Leaderboard(entries=parsed_leaderboard["1"] + parsed_leaderboard["2"] + parsed_leaderboard["3"])


def calc_accuracy(user_input, prompt):
    correct = 0
    for i in range(min(len(user_input), len(prompt))):
        if user_input[i] == prompt[i]:
            correct += 1
    return correct / len(prompt)

def calc_speed(user_input, duration):
    return len(user_input) / duration

def calc_score(accuracy, speed):
    return accuracy ** ACCURACY_WEIGHT * speed

@LogCalls(name=__name__)
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    scoring_pb2_grpc.add_ScoringServiceServicer_to_server(ScoringService(), server)
    server.add_insecure_port('[::]:50055')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()