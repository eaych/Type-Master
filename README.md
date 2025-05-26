# Type Master

### Prerequisites

+ Python 3.10
+ protobuf == 4.25.3
+ grpcio==1.62.0 
+ grpcio-tools==1.62.0 
+ nltk>=3.8.1

## Table of Contents

1. Running the program

1. Client

1. Basic Server
      
    3.1 Basic Prompt Service

    3.2 Basic Scoring Service

1. Advanced Server

    4.1 Advanced Prompt Service
    
    4.2 Advanced Scoring Service


## 1. Running the program

Run `pip install -r requirements.txt` to install prerequisites for Type Master.

After downloading, run `sh build.sh` to build required grpc protobuffers.

A server can be started by running either `basic_server.py` or `adv_server.py`.

A client can be started by running `client.py`. 

## 2. Client

Upon running, the user will be prompted with a selection screen. The user can then input a corresponding number: `1`, `2`, `3` to send commands to the server.

### Commands

#### `1` Start a new challenge

The user inputs their username, desired difficulty and will receive a prompt to copy. After submission, the user will receive statistics and the score will be saved to the server leaderboard.

#### `2` View Scoreboard

Displays the scoreboard, then displays a new selection screen

#### `3` Exit 

Quits the client app.

## 3. Basic Server

### 3.1 Basic Prompt Service

The basic prompt service has responds to the client with a predesigned prompt, one for each difficulty. 

### 3.2 Basic Scoring service

The basic scoring service stores all submitted scores into a local leaderboard, which will then be deleted upon closing the server.

## 4. Advanced Server

### 4.1 Advanced Prompt Service

Requires the `ntlk` library to run. This service responds to the client with a prompt generated and modified from a random phrase from gutenberg.

### 4.2 Advanced Scoring Service

The advanced scoring service stores all submitted scores into a JSON object, which is then stored persistently in a `.json` file

