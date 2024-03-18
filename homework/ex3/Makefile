ARTIFACTS = *pb2.py 
ARTIFACTS += *pb2_grpc.py
ARTIFACTS += *pb2.pyi

all: greet chat

greet:
	python3 -m grpc_tools.protoc -I. --python_out=. --pyi_out=. --grpc_python_out=. greet.proto

chat: 
	python3 -m grpc_tools.protoc -I. --python_out=. --pyi_out=. --grpc_python_out=. chat.proto

.PHONY: clean 

clean:
	rm -f ${ARTIFACTS}