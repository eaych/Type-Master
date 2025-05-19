import grpc
from concurrent import futures
import prompt_pb2_grpc, scoring_pb2_grpc
from prompt_service_basic import *
from scoring_service_basic import *

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    prompt_pb2_grpc.add_PromptServiceServicer_to_server(PromptService(), server)
    scoring_pb2_grpc.add_ScoringServiceServicer_to_server(ScoringService(), server)
    server.add_insecure_port('[::]:50055')
    server.start()
    print("Server running on port 50055...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()