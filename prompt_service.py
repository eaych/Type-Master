import grpc
from concurrent import futures
import prompt_pb2
import prompt_pb2_grpc


class PromptService(prompt_pb2_grpc.PromptServiceServicer):
    def GetPrompt(self, request, context):
        print("got GetPrompt request")

        pre_defined = ["the quick brown fox jumps over the lazy dog",
                       "The quick brown fox 2 jumps over the lazy dog",
                       "The fox jumps over 2 dogs, doesn't it?"]
        
        return prompt_pb2.PromptResponse(prompt=pre_defined[request.level-1])


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    prompt_pb2_grpc.add_PromptServiceServicer_to_server(PromptService(), server)
    server.add_insecure_port('[::]:50055')
    server.start()
    print("Prompt server running on port 50055...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()