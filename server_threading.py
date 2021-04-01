import socket
import threading


def start_server():
    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print('Connected: ', client_address)
            all_clients[client_socket] = [client_address, ]
            print(all_clients)
            thread_listen = threading.Thread(target=listen_client,
                                             args=(client_socket,),
                                             daemon=True)
            thread_listen.start()
            print(threading.enumerate())
    except KeyboardInterrupt:
        for client in all_clients:
            client.send('$SERVER_OFFLINE$'.encode())


def register_client(client_socket):
    print('Registration')
    client_socket.send('Please, enter your name:'.encode())
    name = client_socket.recv(1024)
    all_clients[client_socket].append(name.decode())
    print(all_clients[client_socket])
    welcome_msg = ('Welcome, ' + name.decode() +
                   '. If you want to leave the chat then type \'$Exit\' without quotes')
    print(welcome_msg)
    client_socket.send(welcome_msg.encode())


def listen_client(client_socket):
    print(threading.currentThread().getName() + ' listening is started')
    register_client(client_socket)
    while True:
        msg = client_socket.recv(1024)
        if msg.decode() != '$Exit':
            print(all_clients[client_socket][1], ': ', msg.decode())
            send_to_clients(client_socket, msg)
        else:
            msg_about_disc = all_clients[client_socket][1] + ' disconnected'
            print(msg_about_disc)
            send_to_clients(client_socket, msg_about_disc.encode())
            del all_clients[client_socket]
            client_socket.close()
            break


def send_to_clients(sending_client, msg):
    for client in all_clients:
        if client != sending_client:
            client.send((all_clients[sending_client][1] + ': ').encode() + msg)


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('', 11798))
server_socket.listen()
all_clients = {}
print('Server started')

start_server()