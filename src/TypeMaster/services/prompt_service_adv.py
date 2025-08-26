import grpc
from concurrent import futures
from generated import prompt_pb2, prompt_pb2_grpc

import random

import utils.ntlk_helper as ntlk_helper
from utils.logging import *

MIN_LENGTH = 30
MAX_LENGTH = 120

class PromptService(prompt_pb2_grpc.PromptServiceServicer):
    @LogCalls(name=__name__)
    def GetPrompt(self, request, context):
        generated_text = ""

        while True:
            buffer = []
            generated_text = ntlk_helper.get_random_sentence().replace("\n", " ")

            if request.level == 1:
                for c in generated_text:
                    if c == " " or c.isalpha():
                        buffer.append(c.lower())

                if MIN_LENGTH < len(buffer) < MAX_LENGTH:
                    output = ''.join(buffer)
                    break
                
            elif request.level == 2:
                for c in generated_text:
                    if c == " " or c.isalnum():
                        buffer.append(c)

                if MIN_LENGTH < len(buffer) < MAX_LENGTH and (any(c.isupper() for c in buffer) or any(c.isdigit() for c in buffer)):
                    output = ''.join(buffer)
                    break
            
            elif request.level == 3:
                buffer = generated_text.split(" ")

                if all(all(not c.isdigit() for c in w) for w in buffer):
                    buffer.insert(random.randint(0, len(buffer)), random.choice("1234567890"))

                if MIN_LENGTH < len(' '.join(buffer)) < MAX_LENGTH and any(any(c.isupper() for c in w) for w in buffer) and any(any(not c.isalnum() for c in w) for w in buffer):
                    output = ' '.join(buffer)
                    break
                
        return prompt_pb2.PromptResponse(prompt=output)

@LogCalls(name=__name__, prefix="50055")
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    prompt_pb2_grpc.add_PromptServiceServicer_to_server(PromptService(), server)
    server.add_insecure_port('[::]:50055')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()