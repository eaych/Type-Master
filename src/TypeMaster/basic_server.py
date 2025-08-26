import grpc
from concurrent import futures

from TypeMaster.generated import prompt_pb2_grpc, scoring_pb2_grpc
from TypeMaster.services.prompt_service_basic import *
from TypeMaster.services.scoring_service_basic import *

from utils.logging import *

@LogCalls(name=__name__, prefix="50055")
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    prompt_pb2_grpc.add_PromptServiceServicer_to_server(PromptService(), server)
    scoring_pb2_grpc.add_ScoringServiceServicer_to_server(ScoringService(), server)
    server.add_insecure_port('[::]:50055')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()