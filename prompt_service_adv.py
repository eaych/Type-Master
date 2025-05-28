import grpc
from concurrent import futures
import prompt_pb2, prompt_pb2_grpc

import random

import ntlk_helper
from log_utils import *

MIN_LENGTH = 30
MAX_LENGTH = 120

class PromptService(prompt_pb2_grpc.PromptServiceServicer):
    @LogCalls(name=__name__)
    def GetPrompt(self, request, context):
        generated_text = ""

        while True:
            output = []
            generated_text = ntlk_helper.get_random_sentence().replace("\n", " ")

            if request.level == 1:
                for c in generated_text:
                    if c == " " or c.isalpha():
                        output.append(c.lower())

                if MIN_LENGTH < len(output) < MAX_LENGTH:
                    break
                
            elif request.level == 2:
                for c in generated_text:
                    if c == " " or c.isalnum():
                        output.append(c)

                if MIN_LENGTH < len(output) < MAX_LENGTH and (any(c.isupper() for c in output) or any(c.isdigit() for c in output)):
                    break
            
            elif request.level == 3:
                output = generated_text.split(" ")

                if all(all(not c.isdigit() for c in w) for w in output):
                    output.insert(random.randint(0, len(output)), random.choice("1234567890"))

                if MIN_LENGTH < len(' '.join(output)) < MAX_LENGTH and any(any(c.isupper() for c in w) for w in output) and any(any(not c.isalnum() for c in w) for w in output):
                    break
                
        return prompt_pb2.PromptResponse(prompt=''.join(output))

@LogCalls(name=__name__, prefix="50055")
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    prompt_pb2_grpc.add_PromptServiceServicer_to_server(PromptService(), server)
    server.add_insecure_port('[::]:50055')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()