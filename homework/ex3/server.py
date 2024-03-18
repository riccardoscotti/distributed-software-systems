from concurrent import futures
import grpc 
import greet_pb2, greet_pb2_grpc
import sys

class GreetingService(greet_pb2_grpc.GreetingServiceServicer):
    def Greet(self, request, context) -> greet_pb2.ServerResponse:
        print(f"[Server] Received request from user named '{request.name}'")
        return greet_pb2.ServerResponse(greetingMessage=f"Hello, {request.name}.")

class Server:
    def __init__(self, port: int):
        self.port = port

    def run(self) -> None:
        port = "55555"
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
        greet_pb2_grpc.add_GreetingServiceServicer_to_server(GreetingService(), server)
        server.add_insecure_port("[::]:" + str(self.port))
        server.start()
        print("Server started, listening on " + str(self.port))
        server.wait_for_termination()

if __name__ == "__main__":
    server = Server(int(sys.argv[1]))
    server.run()
    