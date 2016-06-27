from socket import *
import threading
import m_format

BUF_SIZE = 256

class Client:

    def __init__(self):
        self.client_sock = socket(AF_INET, SOCK_STREAM)

        self.write_thread = threading.Thread(target=self.__write_th)
        self.read_thread = threading.Thread(target=self.__read_th)

        self.id = ''

    def __write_th(self):
        message = {"id":self.id, "action":'', "action_value":''}
        while True:
            try:
                msg = raw_input()
                if msg == "exit":
                    pass
                    break
                message["id"] = self.id

                self.client_sock.send(message)
            except Exception as e:
                print e.message
                self.client_sock.close()
                return

    def __read_th(self):
        while True:
            try:
                msg = self.client_sock.recv(m_format.BUF_SIZE)
                message = msg.split('#')

                print "%s : %s"%(message[1], message[2])
            except Exception as e:
                print e.message
                self.client_sock.close()
                return

    def __set_user_info(self):
        id = raw_input("input your name : ")
        self.id = id

    def __connect(self):
        ## set usr id
        ## create or join room
        try:
            self.client_sock.connect(('127.0.0.1', 9097))

            ## set usr id
            self.__set_user_info()
            #### create or join room

            ## recv room info
            self.client_sock.recv(m_format.BUF_SIZE)

            ## recv accepted or denied
            msg = {m_format.ID : self.id, m_format.ACTION : '', m_format.ACTION_VAL : ''}
            while True:
                room = raw_input(self.id+" : ")
                m = m_format.dump(self.id, room)
                self.client_sock.send(m)

                msg = self.client_sock.recv(m_format.BUF_SIZE)
                m = m_format.load(msg)
                action = m[m_format.ACTION]
                action_val = m[m_format.ACTION_VAL]

                if action == m_format.SYS_MSG:
                    if action_val == 'accepted':
                        break
                    elif action_val == 'denied':
                        continue
                else:
                    self.client_sock.close()
                    return false

            return true

        except Exception as e:
            print e.message

    def do(self):
        if self.__connect():
            self.write_thread.start()
            self.read_thread.start()
        else:
            return false

client = Client()
client.do()
