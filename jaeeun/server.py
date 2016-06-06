# -*- coding:utf-8 -*-

from socket import socket
import threading
import json

# id : [사용자 이름]
# action : [create | join | send_msg | broadcast | out ]
# action_value  : [action에 따른 수행 값]

class Server :
    def __init__(self):
        self.server_sock = socket()
        self.clients = []
        self.rooms = {}         #{ room : [clients] }

    def __client_th__(self, client_sock):
        while True :
            data = client_sock.recv()
            protocol = json.loads(data)

            #json 유효성 검사를 해야할듯

            id = protocol['id']
            action = protocol['action']
            value = protocol['action_value']
            response = {'id': id,
                        'action': '',
                        'action_value': ''}
            if action == 'create':
                response['action'] = 'resp'
                if value not in self.rooms:
                    self.rooms[value] = [client_sock]
                    client_sock.room = value
                    response['action_value'] = 'OK'
                else:
                    response['action_value'] = 'ERR'
                client_sock.send(json.dumps(response))
            elif action == 'join':
                response['action'] = 'resp'
                if value in self.rooms:
                    self.rooms[value].append(client_sock)
                    client_sock.room = value
                    response['action_value'] = 'OK'
                else:
                    response['action_value'] = 'ERR'
                client_sock.send(json.dumps(response))
            elif action == 'send_msg':
                response['action'] = action
                response['action_value'] = value
                msg = json.dumps(response)
                if hasattr(client_sock, 'room') :
                    for client in self.rooms :
                        if client != client_sock :
                            client.send(msg)
                else:   #client가 join|craete 후에만 하면 이럴일 없지
                    pass    #잘못된 프로토콜이라는 리스폰을 줄 필요있을까? 프로그래밍 잘못하면 에러가 나지만, 사용자의 반응에 의해 이런 예외가 발생할 일은 없다.
            elif action == 'broadcast':
                response['action'] = action
                response['action_value'] = value
                msg = json.dumps(response)
                for client in self.clients:
                    if client != client_sock :
                        client.send(msg)
            elif action == 'exit':
                if hasattr(client_sock, 'room'):
                    self.rooms[client_sock.room].remove(client_sock)
                    client_sock.close()
            elif action == 'out' :      #방장이 나가면 방장위임문제도 생기네~~
                pass
            else :
                pass # 잘못된 protocol

    def run(self, ip, port, backlog=10):
        self.server_sock.bind((ip, port))
        self.server_sock.listen(backlog)
        while True:
            client = self.server_sock.accept()
            clients.append(client)
            threading.Thread(target=self.__client_th__, args=client[0]).start()


HOST = ''
PORT = 8000

clients = [] #socket list

s = socket()
s.bind((HOST, PORT))
s.listen(10)

while True :
    client_socket = s.accept()
    client_name = client_socket[0].recv(1024) # reccive name
    clients.append(client_socket[0])
    threading.Thread(target=client_th, args=(client_socket[0], client_name)).start()


