import grpc
import scoring_pb2, scoring_pb2_grpc
from concurrent import futures

from log_utils import *
from score_utils import *

class ScoringService(scoring_pb2_grpc.ScoringServiceServicer):
    def __init__(self):
        self.leaderboard = {"1": [], "2": [], "3": []}

    @LogCalls(name=__name__)
    def SubmitResult(self, request, context):

        accuracy = float(calc_accuracy(request.typed_text, request.prompt))
        speed = float(calc_speed(request.typed_text, request.duration))
        score = float(calc_score(accuracy, speed))

        entry = scoring_pb2.LeaderboardEntry(name=request.name, level=request.level, accuracy=accuracy, speed=speed, score=score)

        self.leaderboard[str(request.level)].append(entry)

        self.leaderboard[str(request.level)] = sorted(self.leaderboard[str(request.level)], key=lambda entry: entry.score, reverse=True)[:3]
    
        return scoring_pb2.ScoreResponse(accuracy=accuracy, speed=speed, score=score)

    @LogCalls(name=__name__)
    def GetLeaderboard(self, request, context):
        
        return scoring_pb2.Leaderboard(entries=(self.leaderboard["1"] + self.leaderboard["2"] + self.leaderboard["3"]))

@LogCalls(name=__name__, prefix="50055")
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    scoring_pb2_grpc.add_ScoringServiceServicer_to_server(ScoringService(), server)
    server.add_insecure_port('[::]:50055')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()