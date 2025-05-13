import grpc
from concurrent import futures
import scoring_pb2
import scoring_pb2_grpc

class Scoring(scoring_pb2_grpc.ScoringServiceServicer):
    def Echo(self, request, context):
        return scoring_pb2.EchoResponse(message=request.message)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    scoring_pb2_grpc.add_EchoServiceServicer_to_server(EchoService(), server)
    server.add_insecure_port('[::]:50055')
    server.start()
    print("Echo server running on port 50055...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
