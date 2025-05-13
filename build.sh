python -m grpc_tools.protoc -I protobufs --python_out=. --grpc_python_out=. protobufs/scoring.proto
python -m grpc_tools.protoc -I protobufs --python_out=. --grpc_python_out=. protobufs/prompt.proto