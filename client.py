import socket
import threading


def receive_msg():
    try:
        while True:
            data = client_socket.recv(1024)
            print(data.decode())
    except ConnectionAbortedError:
        pass


def client_send():
    thread_rcv = threading.Thread(target=receive_msg)
    thread_rcv.start()
    try:
        while True:
            msg = str(input())
            client_socket.send(msg.encode())
            if msg == '$Exit':
                break
    except KeyboardInterrupt:
        pass


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 11719))
print(client_socket.recv(1024).decode())
client_socket.send(input().encode())

client_send()
client_socket.close()
