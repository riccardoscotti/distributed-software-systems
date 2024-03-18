from threading import Thread
from concurrent import futures
import grpc 
import greet_pb2, greet_pb2_grpc
import chat_pb2, chat_pb2_grpc
from time import sleep
from datetime import datetime
import sys

TIME_FORMAT = '%H:%M'

class ChatService(chat_pb2_grpc.ChatServiceServicer):
    def __init__(self, name: str) -> None:
        super()
        self.name = name
    
    def SendMessage(self, request, context):
        if(request.body):
            
            print(f'\u001b[1;36m[{request.time}] {request.senderName}>\u001b[0m {request.body}')
        return chat_pb2.Nothing()
    
    def GetInfo(self, request, context):
        return chat_pb2.ChatMessage(time=datetime.now().strftime(TIME_FORMAT), senderName=self.name, body='OK')


class Client:
    def __init__(self, name: str, sendingPort: int, listeningPort: int = None) -> None:
        self.name = name 
        self.sendingPort = sendingPort
        self.listeningPort = listeningPort
    
    def connect_to_server(self) -> None:
        with grpc.insecure_channel(f'localhost:{self.sendingPort}') as channel:
            stub = greet_pb2_grpc.GreetingServiceStub(channel)
            response = stub.Greet(greet_pb2.UserInfo(name=self.name))
        print(f'[{self.name}] Message received from server: "{response.greetingMessage}"')

    def listen(self) -> None:
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
        chat_pb2_grpc.add_ChatServiceServicer_to_server(ChatService(self.name), server)
        server.add_insecure_port("[::]:" + str(self.listeningPort))
        server.start()
        
        server.wait_for_termination()

    def chat(self) -> None:
        with grpc.insecure_channel(f'localhost:{self.sendingPort}') as channel:
            stub = chat_pb2_grpc.ChatServiceStub(channel)

            peerName = None
            connected = False 
            print('\u001b[1;94mWaiting for other peer to connect...\u001b[0m')
            while not connected:
                try:
                    peerName = stub.GetInfo(chat_pb2.Nothing()).senderName
                    connected = True
                except:
                    sleep(3)
            
            print(f'\n\n\u001b[1;94mWelcome, \u001b[1;32m{self.name}\u001b[1;94m. You are chatting with \u001b[1;36m{peerName}\u001b[1;94m.\u001b[0m\n\n')

            while True:
                message = input()
                try:
                    if(message):
                        stub.SendMessage(chat_pb2.ChatMessage(time=datetime.now().strftime(TIME_FORMAT), senderName=self.name, body=message))
                        print(f'\u001b[1A\u001b[2K\u001b[1;32m[{datetime.now().strftime(TIME_FORMAT)}] {self.name}>\u001b[0m {message}')
                except:
                    print('\u001b[1;94mOther peer unreachable. Future messages may be lost.\u001b[0m')

    


if __name__ == "__main__":
    listeningPort = int(sys.argv[1])
    client1 = Client('Alice', listeningPort)
    client2 = Client('Bob', listeningPort)

    print("Client 1 started")
    Thread(target=client1.connect_to_server).start()
    
    print("Client 2 started")
    Thread(target=client2.connect_to_server).start()

    