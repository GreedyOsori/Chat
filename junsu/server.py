from socket import *
import threading
import m_format
import message


class Server:
    def __init__(self):
        HOST = ''
        PORT = m_format.PORT

        self.server_sock = socket(AF_INET, SOCK_STREAM)
        self.server_sock.bind((HOST, PORT))
        self.server_sock.listen(5)

        self.d_room_client = {}
        self.d_client_info = {}

        print ('Server socket is binded... ')
        print ('Ready!!!')

    def __broadcast(self, client_sock, msg):
        pass

    def __send_to_room(self, client_sock, msg):

        ## msg is already formatted
        c_id, room, master = self.d_client_info[client_sock]

        print msg

        # client = { room_num : [](client_list)}
        for c_sock, c_addr in self.d_room_client[room]:
            if c_sock != client_sock:
                try:
                    c_sock.send(msg)
                except Exception as e:
                    print (e.message)
                    self.__handle_client_exit()

    ## return Bool : True or False
    def __accept_client(self, client_sock, client_addr):
        try:
            ## debug

            tmp_m = "room list : " + str(self.d_room_client.keys()) + "\ncreate room : ex) create#room_name\njoin room : ex) join#room_name\nexit : ex) exit#"
            client_sock.send(tmp_m)

            while True:
                msg = client_sock.recv(m_format.BUF_SIZE)
                m = m_format.load(msg)
                ## debug
                print m

                c_id = m[m_format.ID]
                action = m[m_format.ACTION]
                action_val = m[m_format.ACTION_VAL]

                if action == m_format.CREATE:
                    ## if room name is already exist
                    if action_val in self.d_room_client.keys():
                        msg = m_format.dump('', "sys_msg#denied")
                        client_sock.send(msg)
                        continue
                    msg = m_format.dump('', "sys_msg#accepted")
                    client_sock.send(msg)
                    self.d_room_client[action_val] = [(client_sock, client_addr)]
                    self.d_client_info[client_sock] = (c_id , action_val, True)
                    return True

                elif action == m_format.JOIN:
                    if action_val in self.d_room_client.keys():
                        msg = m_format.dump('', "sys_msg#accepted")
                        client_sock.send(msg)
                        self.d_room_client[action_val].append((client_sock, client_addr))
                        self.d_client_info[client_sock] = (c_id, action_val, False)
                        return True
                    else:
                        msg = m_format.dump('', "sys_msg#denied")
                        client_sock.send(msg)
                        continue

                elif action == m_format.EXIT:
                    client_sock.close()
                    return False
                else:
                    msg = m_format('', "sys_msg#denied")
                    client_sock.send(msg)

        except Exception as e:
            print "erororoorororororoor"
            print (e.message)
            client_sock.close()

    def __handle_client_exit(self, client_sock, client_addr):
        c_id, room, master = self.d_client_info[client_sock]
        self.d_room_client[room].remove((client_sock, client_addr))
        self.d_client_info.pop(client_sock)
        client_sock.close()

    def __serve_client(self, client_sock, client_addr):
        # recv "create" or "join"
        # d_room_client, d_client_room is
        if not self.__accept_client(client_sock, client_addr):
            return

        print "chatting is start!!"
        while True:
            try:
                msg = client_sock.recv(m_format.BUF_SIZE)
                ## disconnection unexepectedly
                if not msg:
                    print "disconnected??"
                    self.__handle_client_exit(client_sock, client_addr)
                    return
                m = m_format.load(msg)
                print "message : " + str(m)
                action = m[m_format.ACTION]

                print "get item is done"

                if action == m_format.SEND_MSG:
                    self.__send_to_room(client_sock, msg)
                elif action == m_format.BROADCAST:
                    self.__broadcast(client_sock, msg)
                elif action == m_format.EXIT:
                    msg = m_format.dump(m[m_format.ID], "sys_msg#"+m[m_format.ID]+" quit chatting")
                    self.__send_to_room(client_sock, msg)
                    self.__handle_client_exit(client_sock, client_addr)
                elif action == m_format.OUT:
                    pass

            except Exception as e:
                print (e.message)
                self.__handle_client_exit(client_sock,client_addr)

    def do(self):
        while True:
            print ('Waiting for Client ......')
            client = self.server_sock.accept()
            ##print ('Client(%s) is connected !!\n' % str(client[1]))
            print "Client is connected!"

            client_th = threading.Thread(target=self.__serve_client, args=client)
            client_th.start()

        client_th.join()


server = Server()
server.do()
