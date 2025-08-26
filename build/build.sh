python -m grpc_tools.protoc -I=../proto --python_out=../src/TypeMaster/generated --grpc_python_out=../src/TypeMaster/generated ../proto/scoring.proto ../proto/prompt.proto

cat <<EOF

-- WARNING --

GENERATED FILES REBUILT.

GO TO 
    src/TypeMaster/generated/prompt_pb2_grpc.py
    src/TypeMaster/generated/scoring_pb2_grpc.py

AND REPLACE LINES
    import prompt_pb2 as prompt__pb2
    import scoring_pb2 as scoring__pb2
WITH
    import TypeMaster.generated.prompt_pb2 as prompt__pb2
    import TypeMaster.generated.scoring_pb2 as scoring__pb2
RESPECTIVELY.

EOF