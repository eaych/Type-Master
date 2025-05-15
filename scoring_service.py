import grpc
from concurrent import futures
import scoring_pb2
import scoring_pb2_grpc


ACCURACY_WEIGHT = 1.4

'''
message TypingResult {
  string name = 1;
  int32 level = 2;
  string prompt = 3;
  string typed_text = 4;
  float duration = 5; // time in seconds
}

message ScoreResponse {
  float accuracy = 1;
  float speed = 2;
  float score = 3;
}
'''

class ScoringService(scoring_pb2_grpc.ScoringServiceServicer):
    def SubmitResult(self, request, context):
        print("got SubmitResult request")

        accuracy = calc_accuracy(request.typed_text, request.prompt)
        speed = calc_speed(request.typed_text, request.duration)
        score = calc_score(accuracy, speed)

        # TODO: send data to leaderboard

        return scoring_pb2.ScoreResponse(accuracy=accuracy, speed=speed, score=score)

    def GetLeaderboard(self, request, context):
        print("got GetLeaderboard request")

        return scoring_pb2.GetLeaderboard()


def calc_accuracy(user_input, prompt):
    correct = 0
    for i in range(min(len(user_input), len(prompt))):
        if user_input[i] == prompt[i]:
            correct += 1
    return correct / len(prompt)

def calc_speed(user_input, duration):
    return len(user_input) / duration

def calc_score(accuracy, speed):
    return accuracy ** ACCURACY_WEIGHT * speed

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    scoring_pb2_grpc.add_ScoringServiceServicer_to_server(ScoringService(), server)
    server.add_insecure_port('[::]:50055')
    server.start()
    print("Prompt server running on port 50055...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()