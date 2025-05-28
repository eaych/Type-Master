# Type Master

### Prerequisites

+ Python 3.10
+ protobuf==4.25.3
+ grpcio==1.62.0 
+ grpcio-tools==1.62.0 
+ nltk>=3.8.1

## Table of Contents 

1. [Running the program](#1-running-the-program)

1. [Client](#2-client)

1. [Basic Server](#3-basic-server)
      
    3.1 [Basic Prompt Service](#31-basic-prompt-service)

    3.2 [Basic Scoring Service](#32-basic-scoring-service)

1. [Advanced Server](#4-advanced-server)

    4.1 [Advanced Prompt Service](#41-advanced-prompt-service)
    
    4.2 [Advanced Scoring Service](#42-advanced-scoring-service)

## 1. Running the program

Run `pip install -r requirements.txt` to install prerequisites for Type Master.

After downloading prerequisites, run `build.sh` to build required grpc stubs.

A server can be started by running either `basic_server.py` or `adv_server.py`.

A client can be started by running `client.py`. 

By default, the program will create and log service calls in `server.log`.

## 2. Client

> Upon running, the user will be prompted with a selection screen. The user can then input a corresponding number: `1`, `2`, `3` to send commands to the server. Invalid inputs are ignored.

### Commands

#### `1` Start a new challenge

The user inputs their username, desired difficulty and will receive a prompt to copy. After submission, the user will receive statistics and the score may be saved to the server leaderboard.

#### `2` View Scoreboard

Displays the scoreboard, then displays a new selection screen

#### `3` Exit 

Quits the client app.

## 3. Basic Server

### 3.1 Basic Prompt Service

> The basic prompt service has responds to the client with a predesigned prompt, one for each difficulty. 

Basic `PromptService` contains the method: 

`GetPrompt()`, which takes a `LevelRequest` object, containing the desired level, as a parameter. Responds with a `PromptResponse` object, containing the corresponding prompt.

### 3.2 Basic Scoring service

> The basic scoring service stores the 3 best submitted scores of each diffculty level into a local leaderboard, which will then be deleted upon closing the server.

Basic `ScoringService` contains the methods:

`SubmitResult()`, which takes a `TypingResult` object containing the information `name`, `level`, `score`, `accuracy`, `speed`. If the submitted result's score is within the top 3 of its respective level, it will then be stored in the leaderboard. Responds with a `ScoreResult` object, containing the submitted score's accuracy, score, and speed.

`GetLeaderboard()`, which takes an `Empty` object as a parameter. Responds with a `Leaderboard` object, containing up to 9 `LeaderboardEntry` objects, each containing a name, level, score, accuracy, and speed.

## 4. Advanced Server 

### 4.1 Advanced Prompt Service

> Requires the `ntlk` library to run. This service responds to the client with a prompt generated and modified from a random phrase from gutenberg.

Advanced `PromptService` contains the method: 

`GetPrompt()`, which takes a `LevelRequest` object, containing the desired level, as a parameter. Responds with a `PromptResponse` object, containing a string generated on request which may be modified to fit the desired difficulty level.

### 4.2 Advanced Scoring Service

> The advanced scoring service stores all submitted scores as a JSON object, which is then stored persistently in a `leaderboard.json` file. Upon starting the server, it will read and store the JSON object as a dictionary, which will be modified as needed before writing to persistent storage whenever a score is submitted. If `leaderboard.json` does not exist, it will automatically be created and filled with an empty object.

Advanced `ScoringService` contains the methods:

`SubmitResult()`, which takes a `TypingResult` object, containing the information `name`, `level`, `score`, `accuracy`, `speed`. If the submitted result's score is within the top 3 of its respective level, it will then be stored in `Leaderboard`. Responds with a `ScoreResult` object, containing the submitted score's accuracy, score, and speed.

`GetLeaderboard()`, which takes an `Empty` object. Responds with a `Leaderboard` object, containing up to 9 `LeaderboardEntry` objects, each containing a name, level, score, accuracy, and speed.

