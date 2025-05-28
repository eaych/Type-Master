import grpc
import json
from log_utils import *
from concurrent import futures
import prompt_pb2_grpc, scoring_pb2_grpc
from prompt_service_adv import *
from scoring_service_adv import *

@LogCalls(name=__name__)
def serve():
    try:
        with open("leaderboard.json", "x") as f:
           json.dump({"1": [], "2": [], "3": []}, f) 
    except:
        pass
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    prompt_pb2_grpc.add_PromptServiceServicer_to_server(PromptService(), server)
    scoring_pb2_grpc.add_ScoringServiceServicer_to_server(ScoringService(), server)
    server.add_insecure_port('[::]:50055')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()