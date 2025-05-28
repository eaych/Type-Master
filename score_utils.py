ACCURACY_WEIGHT = 1.4

def calc_accuracy(user_input, prompt):
    correct = 0
    for i in range(min(len(user_input), len(prompt))):
        if user_input[i] == prompt[i]:
            correct += 1
    return correct / len(prompt) * 100

def calc_speed(user_input, duration):
    return len(user_input) / duration

def calc_score(accuracy, speed):
    return accuracy ** ACCURACY_WEIGHT * speed