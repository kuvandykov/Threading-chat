import socket
import threading


def receive_msg():
    while True:
        try:
            data = client_socket.recv(1024)
            print(data.decode())
            if data.decode() == '$SERVER_OFFLINE$':
                break
        except ConnectionAbortedError:
            break


def client_send():
    thread_rcv = threading.Thread(target=receive_msg, daemon=True)
    thread_rcv.start()
    try:
        while True:
            msg = str(input())
            client_socket.send(msg.encode())
            if msg == '$Exit':
                break
    except KeyboardInterrupt:
        client_socket.send('$Exit'.encode())
    except BrokenPipeError:
        pass


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 11798))
print(client_socket.recv(1024).decode())
client_socket.send(input().encode())

client_send()
client_socket.close()
