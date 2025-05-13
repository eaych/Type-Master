import grpc
import prompt_pb2
import prompt_pb2_grpc
import scoring_pb2
import scoring_pb2_grpc
from display import *

def run():
    with grpc.insecure_channel('localhost:50055') as channel:
        Prompt = prompt_pb2_grpc.PromptServiceStub(channel)
        Scoring = scoring_pb2_grpc.ScoringServiceStub(channel)

        print(selection_screen)
        command = int(input(""))

        response = Prompt.GetPrompt(prompt_pb2.LevelRequest(level=command))

        print(prompt_display.format(prompt = response.prompt))

if __name__ == '__main__':
    run()
