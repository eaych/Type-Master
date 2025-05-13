import grpc
import ntlk_helper
from concurrent import futures
import prompt_pb2
import prompt_pb2_grpc


class PromptService(prompt_pb2_grpc.PromptServiceServicer):
    def GetPrompt(self, request, context):
        print("got request")
        output = []
        generated_text = ntlk_helper.get_random_sentence().replace("\n", " ").split()
        print(generated_text)
        if request.level == 1:
            print(generated_text)

        return prompt_pb2.PromptResponse(prompt=''.join(output))

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    prompt_pb2_grpc.add_PromptServiceServicer_to_server(PromptService(), server)
    server.add_insecure_port('[::]:50055')
    server.start()
    print("Prompt server running on port 50055...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()


'''
a a a a a
a a a a a a

'''