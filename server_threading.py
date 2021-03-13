import socket
import threading


def server_start():
    while True:
        client_socket, client_address = server_socket.accept()
        print('Connected:', client_address)
        thread_reg = threading.Thread(target=register_client, args=(client_socket, client_address,))
        thread_reg.start()
        thread_listen = threading.Thread(target=listen_client, args=(client_socket, ))
        thread_listen.start()


def register_client(client, client_adr):
    client.send('Please, enter your name:'.encode())
    name = client.recv(1024)
    tmp = 'Welcome, ' + name.decode() + '. If you want to leave the chat then type \'$Exit\' without quotes'
    client.send(tmp.encode())
    clients[client] = (name.decode(), client_adr)
    sent_msgs(name.decode() + ' joined', client, mode=1)
    print(clients[client][1], ' is ', clients[client][0])


def listen_client(client):
    while True:
        try:
            msg = client.recv(1024)
            msg = msg.decode()
            if msg != '$Exit':
                print(msg)
                sent_msgs(msg, client)
            else:
                msg_about_disc = clients[client][0] + ' disconnected'
                print(clients[client][1], ' disconnected')
                sent_msgs(msg_about_disc, client, disc_msg=True)
                del clients[client]
                client.close()
                break
        except socket.error:
            msg_about_disc = clients[client][0] + ' disconnected'
            print(clients[client][1], ' disconnected')
            sent_msgs(msg_about_disc, client, disc_msg=True)
            del clients[client]
            client.close()
            break


def sent_msgs(data, from_client, disc_msg=False, mode=0):
    if disc_msg:
        msg = data
    else:
        msg = clients[from_client][0] + ' sent: ' + data
    for clnt in clients:
        if clients[clnt] != clients[from_client]:
            if mode == 0:
                clnt.send(msg.encode())
            elif mode == 1:
                clnt.send((clients[from_client][0] + ' joined').encode())


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 11719))
server_socket.listen(5)
print('Server started')

clients = {}

if __name__ == '__main__':
    server_start()
