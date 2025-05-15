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

        # TODO: Clean up code
        if command == 1:
            # Play a round
            user_name = input("ENTER NAME: ")
            level = int(input(difficulty_select))

            prompt = Prompt.GetPrompt(prompt_pb2.LevelRequest(level=level))

            input(prompt_display.format(prompt = prompt.prompt))
            
            start = time.time()
            user_input = input()
            end = time.time()
            duration = end - start

            results = Scoring.SubmitResult(scoring_pb2.TypingResult(name=user_name, level=level, prompt=prompt.prompt, typed_text=user_input, duration=duration))
            
            print(results.accuracy, results.score, results.speed)


if __name__ == '__main__':
    run()
