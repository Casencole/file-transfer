# Casen Cole 10/23/24
# Based on https://thepythoncode.com/article/send-receive-files-using-sockets-python
# Should be able to recive files sent from a client

import os
import socket

import tqdm

BUFFER_SIZE = 4096          # Amount of bytes in each recv
HOST        = "127.0.0.0"
PORT        = 65432
SEPARATOR   = "<SEP>"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # bind socket to local address
    s.bind((HOST, PORT))

    # accept any connections
    s.listen()
    conn, addr = s.accept()

    #recive file info
    fileInfo = conn.recv(BUFFER_SIZE).decode()
    filename, filesize = fileInfo.split(SEPARATOR)
    filename = os.path.basename(filename) # only keep basename of file is absolute path
    filesize = int(filesize)

    #start reciveing file from the connection
    progress = tqdm.tqdm(range(filesize), f"Reciveing {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "wb") as f:
        while True:
            bytesRead = conn.recv(BUFFER_SIZE)
            if not bytesRead:
                # file is done sending
                break
            f.write(bytesRead)
            progress.update(len(bytesRead))
    conn.close()
