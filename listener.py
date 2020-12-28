import socket
import json
import threading


def listen():
    class ClientThread(threading.Thread):
        def __init__(self, address, client):
            threading.Thread.__init__(self)
            self.client = client

        def run(self):
            while True:
                try:
                    command = client.recv(1024).decode('utf-8')
                    if command == secret_command:
                        client.send(f"You probably thought to yourself [{flag}] but you done it!".encode('utf-8'))
                    else:
                        client.send(f"command {command} unidentified".encode('utf-8'))
                except socket.error:
                    break
            client.close()
            return

    with open('config.json') as f:
        content = json.load(f)

    # host = content["ip"]
    port = int(content["port"])
    secret_command = content["command"]
    flag = content["flag"]

    host = '127.0.0.1'  # '159.65.202.70'

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))

    while True:
        server.listen()

        try:
            client, address = server.accept()
            thread = ClientThread(address, client)
            thread.start()
        except:
            continue





# def listen():
#     with open('config.json') as f:
#         content = json.load(f)
#
#     # host = data["ip"]
#     port = int(content["port"])
#     secret_command = content["command"]
#     flag = content["flag"]
#
#     host = '127.0.0.1'  # '159.65.202.70'
#
#     server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server.bind((host, port))
#
#     server.listen()
#
#     while True:
#         # error handling for unexpected client connection termination
#         try:
#             client, address = server.accept()
#         except socket.error as msg:
#             server.close()
#             continue
#
#         try:
#             command = client.recv(1024).decode('utf-8')
#             if command == secret_command:
#                 client.send(f"sure you thought to yourself [{flag}] but you done it!".encode('utf-8'))
#             else:
#                 client.send(f"command {command} unidentified".encode('utf-8'))
#         except socket.error as msg:
#             print(msg)

