import grpc
import time
import prompt_pb2, prompt_pb2_grpc, scoring_pb2, scoring_pb2_grpc
from display import *

def run():
    with grpc.insecure_channel('localhost:50055') as channel:
        Prompt = prompt_pb2_grpc.PromptServiceStub(channel)
        Scoring = scoring_pb2_grpc.ScoringServiceStub(channel)
        
        while True:
            command = int(input(selection_screen))

            if command == 3:
                break

            # TODO: Clean up code
            elif command == 1:
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
            
            elif command == 2:
                
                results = Scoring.GetLeaderboard(scoring_pb2.Empty())

                scores = {"1": [], "2": [], "3": []}
                for entry in results.entries:

                    scores[entry.level].append(
                        leaderboard_entry.format(
                            score=entry.score,
                            accuracy=entry.accuracy*100,
                            speed=entry.speed,
                            name=entry.name
                        )
                    )

                print(leaderboard_display.format(
                    easy_scores='\n\t'.join(scores[1]),
                    medium_scores='\n\t'.join(scores[2]),
                    hard_scores='\n\t'.join(scores[3])
                ))

if __name__ == '__main__':
    run()
