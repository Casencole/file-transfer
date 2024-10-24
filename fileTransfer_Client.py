# Casen Cole 10/23/2024
# Based off of https://thepythoncode.com/article/send-receive-files-using-sockets-python
# This client should be able to send file to a server

import os
import socket
import sys

import tqdm  # Magic progress bar

SEPARATOR = "<SEP>"
BUFFER_SIZE = 4096  # send BUFFER_SIZE bytes each send

HOST = "127.0.0.0"
PORT = 65432

#TODO add a for loop so it can send multiple files that are passe

# Indentation as a form of {} is crazy I never thought I would miss C
filename     = sys.argv[1]
if not os.path.isfile(filename):
    print("File was not found\n")
    sys.exit()

filesize = os.path.getsize(filename)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))


    # senf file name & size
    s.send(f"{filename}{SEPARATOR}{filesize}".encode())

    # Fancy progress bar that I don't fully understand
    progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)

    with open(filename, "rb") as f:
        while True:
            bytesRead = f.read(BUFFER_SIZE)
            if not bytesRead:
                # file is done sending
                break

            # sendall is safter is busy networks?
            s.sendall(bytesRead)
            # and update the magic progress bar
            progress.update(len(bytesRead))
