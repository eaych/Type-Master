import grpc
import ntlk_helper
from concurrent import futures
import prompt_pb2
import prompt_pb2_grpc


class PromptService(prompt_pb2_grpc.PromptServiceServicer):
    def GetPrompt(self, request, context):
        print("got request")
        generated_text = ""

        while True:
            output = []
            generated_text = ntlk_helper.get_random_sentence().replace("\n", " ")

            print(generated_text)

            if request.level == 1:
                for c in generated_text:
                    if c == " " or c.isalpha():
                        output.append(c.lower())

                if 20 < len(output) < 120:
                    return prompt_pb2.PromptResponse(prompt=''.join(output))
                
            elif request.level == 2:
                for c in generated_text:
                    if c == " " or c.isalnum():
                        output.append(c)

                if 20 < len(output) < 120 and (any(c.isupper() for c in output) or any(c.isdigit() for c in output)):
                    return prompt_pb2.PromptResponse(prompt=''.join(output))
            
            elif request.level == 3:
                output = list(generated_text)

                if 20 < len(output) < 120 and any(c.isupper() for c in output) and any(c.isdigit() for c in output) and any(not c.isalnum() for c in output):
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