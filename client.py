import grpc
import time
import prompt_pb2
import prompt_pb2_grpc
import scoring_pb2
import scoring_pb2_grpc
from display import *

def run():
    with grpc.insecure_channel('localhost:50055') as channel:
        Prompt = prompt_pb2_grpc.PromptServiceStub(channel)
        Scoring = scoring_pb2_grpc.ScoringServiceStub(channel)

        command = int(input(selection_screen))

        if command == 1:
            # Play a round
            user_name = input("ENTER NAME: ")
            level = int(input(difficulty_select))

            prompt = Prompt.GetPrompt(prompt_pb2.LevelRequest(level=level))

            input(prompt_display.format(prompt = prompt.prompt))
            
            start = time.time()
            user_input = input()
            end = time.time()
            speed = end - start

            correct = 0
            for i in range(min(len(user_input), len(prompt.prompt))):
                if user_input[i] == prompt.prompt[i]:
                    correct += 1
            accuracy = correct / len(prompt.prompt)


            print(speed, accuracy)



if __name__ == '__main__':
    run()
