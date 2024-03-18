import sys 
import os 
import time 
import daemon
import logging
from datetime import datetime

def watch_dir(selected_path):
    files = set() 

    # setting up the logger
    logging.basicConfig(
        filename='./dirwatcher.log', 
        encoding='utf-8', 
        level=logging.DEBUG,
        format='%(message)s')
    
    # the daemon (theoretically) runs indefinitely, hence the while True
    while True: 
        # iterating over all items in the selected directory
        for file in os.listdir(selected_path):
            # checking if the item is a file
            file_path = os.path.join(selected_path, file)
            if os.path.isfile(file_path):
                # if file was not already in the set, it is added and then logged
                if file_path not in files:
                    files.add(file_path)
                    time_added = datetime.fromtimestamp(os.path.getctime(file_path)).strftime('%d/%m/%Y %H:%M:%S')
                    logging.debug(f'[{time_added}] File named "{file}" added')
        time.sleep(10)

if __name__ == '__main__':
    # the directory to monitor is passed as a command-line argument
    path = sys.argv[1]

    # daemonization of watch_dir function
    with daemon.DaemonContext() as context:
        watch_dir(path)
    
    

    
