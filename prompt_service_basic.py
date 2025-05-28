import grpc
import logging
from concurrent import futures
from log_utils import *
import prompt_pb2, prompt_pb2_grpc

logger = logging.getLogger(__name__)

class PromptService(prompt_pb2_grpc.PromptServiceServicer):
    @LogCalls(name=__name__)
    def GetPrompt(self, request, context):
        logger.debug('Request received')

        pre_defined = ["the quick brown fox jumps over the lazy dog",
                       "The quick brown fox 2 jumps over the lazy dog",
                       "The fox jumps over 2 dogs, doesn't it?"]
        
        return prompt_pb2.PromptResponse(prompt=pre_defined[request.level-1])

@LogCalls(name=__name__)
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    prompt_pb2_grpc.add_PromptServiceServicer_to_server(PromptService(), server)
    server.add_insecure_port('[::]:50055')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()