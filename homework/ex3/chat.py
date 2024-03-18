import sys 
from client import Client
from threading import Thread

if __name__ == "__main__":
    peer = Client(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
    listener = Thread(target=peer.listen)
    sender = Thread(target=peer.chat)

    listener.start()
    sender.start()
    listener.join()
    sender.join()
    
    
