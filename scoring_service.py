import grpc
from concurrent import futures
import scoring_pb2
import scoring_pb2_grpc


class ScoringService(scoring_pb2_grpc.ScoringServiceServicer):
    def SubmitResult(self, request, context):
        print("got SubmitResult request")

        return scoring_pb2.ScoreResponse()

    def GetLeaderboard(self, request, context):
        print("got GetLeaderboard request")

        return scoring_pb2.GetLeaderboard()


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    scoring_pb2_grpc.add_ScoringServiceServicer_to_server(ScoringService(), server)
    server.add_insecure_port('[::]:50055')
    server.start()
    print("Prompt server running on port 50055...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()