from socket import *
import threading
import m_format
import message

class Server:

    def __init__(self):
        HOST = ''
        PORT = 9097

        self.server_sock = socket(AF_INET, SOCK_STREAM)
        self.server_sock.bind((HOST, PORT))
        self.server_sock.listen(5)

        self.d_room_client = {}
        self.d_client_room = {}

        print "Server socket is binded ...... PORT : "+ str(PORT)
        print "Ready!!!"

    def __broadcast(self, client_sock, msg):
        room = self.d_client_room[client_sock]

        # client = { room_num : [](client_list)}
        for c_sock, c_addr in self.d_room_client[room]:
            if(c_sock != client_sock):
                try:
                    m.send_msg(c_sock,msg)
                except Exception as e:
                    print e.message
                    c_sock.close()
                    pass

    ## return Bool : True or False
    def __accept_client(self, client_sock, clinet_addr):
        try:
            client_sock.send(str(self.d_room_client.keys())+"\ncreate room : ex) create#room_name\njoin room : ex) join#room_name"+"\nexit : ex) exit#")
            while True:
                msg = client_sock.recv(256)
                m = m_format.load(msg)
                action = m[m_format.ACTION]
                action_val = m[m_format.ACTION_VAL]

                if action == m_format.CREATE:
                    ## if room name is already exist
                    if action_val in self.d_room_client.keys():
                        msg = m_format.dump('', "sys_msg#denied")
                        client_sock.send(msg)
                        continue
                    msg = m_format.dump('',"sys_msg#accepted")
                    client_sock.send(msg)
                    self.d_room_client[action_val] = [(client_sock,clinet_addr)]
                    self.d_client_room[client_sock] = action_val
                    return True

                elif action == m_format.JOIN:
                    if action_val in self.d_room_client.keys():
                        msg = m_format.dump('',"sys_msg#accepted")
                        client_sock.send(msg)
                        self.d_room_client[action_val].append((client_sock,clinet_addr))
                        self.d_client_room[client_sock] = action_val
                        return True
                    else:
                        msg = m_format.dump('', "sys_msg#denied")
                        client_sock.send(msg)
                        continue

                elif action == m_format.EXIT:
                    client_sock.close()
                    return False
                    ## if room is not available,

        except Exception as e:
            print e.message
            client_sock.close()


    def __serve_client(self, client_sock, client_addr):
        # recv "create" or "join"
        # d_room_client, d_client_room is
        if not self.__accept_client(client_sock, client_addr):
            return
        while True:
            try:
                msg = m.recv_msg(client_sock)
                ## disconnection unexepectedly
                if not msg:

                    ## this part -> make function
                    room = self.d_client_room[client_sock]
                    self.d_room_client[room].remove((client_sock,client_addr))
                    self.d_client_room.pop(client_sock)
                    client_sock.close()
                    ####### handle client_exit()
                    return
            except Exception as e:
                print e.message
                room = self.d_client_room[client_sock]
                self.d_room_client[room].remove((client_sock, client_addr))
                self.d_client_room.pop(client_sock)
                client_sock.close()

            self.__broadcast(client_sock, msg)

    def do(self):
        while True:
            print 'Waiting for Client ......'
            client = self.server_sock.accept()
            print 'Client(%s) is connected !!\n'% (client[1])

            client_th = threading.Thread(target=self.__serve_client,args = client)
            client_th.start()

        client_th.join()


server = Server()
server.do()


