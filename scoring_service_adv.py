import grpc
import json
from concurrent import futures
import scoring_pb2, scoring_pb2_grpc


ACCURACY_WEIGHT = 1.4

class ScoringService(scoring_pb2_grpc.ScoringServiceServicer):
    def SubmitResult(self, request, context):
        print("got SubmitResult request")

        accuracy = float(calc_accuracy(request.typed_text, request.prompt))
        speed = float(calc_speed(request.typed_text, request.duration))
        score = float(calc_score(accuracy, speed))

        entry = {"name": request.name, "level": request.level, "accuracy": accuracy, "speed": speed, "score": score}
        entry_json = json.dumps(entry)

        try:
            with open("leaderboard.json", "w") as f:
                f.write(entry_json)
        except:
            with open("leaderboard.json", "x") as f:
                f.write(entry_json)
        
        return scoring_pb2.ScoreResponse(accuracy=accuracy, speed=speed, score=score)

    def GetLeaderboard(self, request, context):
        print("got GetLeaderboard request")

        try:
            with open("leaderboard.json", "w") as f:
                f.write(entry_json)
        except:
            with open("leaderboard.json", "x") as f:
                f.write(entry_json)
        
        return scoring_pb2.Leaderboard(entries=(self.leaderboard[1] + self.leaderboard[2] + self.leaderboard[3]))


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

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    scoring_pb2_grpc.add_ScoringServiceServicer_to_server(ScoringService(), server)
    server.add_insecure_port('[::]:50055')
    server.start()
    print("Scoring server running on port 50055...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()