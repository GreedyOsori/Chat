from socket import *
import threading
import m_format
import time

class Client:

    def __init__(self):
        self.client_sock = socket(AF_INET, SOCK_STREAM)

        self.write_thread = threading.Thread(target=self.__write_th)
        self.read_thread = threading.Thread(target=self.__read_th)

        self.id = ''

    def __write_th(self):
        while True:
            try:
                msg = raw_input()
                m = m_format.dump(self.id, msg)

                self.client_sock.send(m)

                msg = m_format.load(m)
                if msg[m_format.ACTION] == m_format.EXIT:

                    ## same ip addr can be accepted in this test
                    ## so can't set d_client_info's key - client_addr //
                    ## but if key is client_sock,
                    ## in case that cleint_sock close first, and server refer socket
                    ## it'll have trash val
                    ## so sleep ....
                    time.sleep(2)
                    self.client_sock.close()

            except Exception as e:
                print (e.message)
                self.client_sock.close()
                return

    def __read_th(self):
        while True:
            try:
                msg = self.client_sock.recv(m_format.BUF_SIZE)
                if msg == '':
                    time.sleep(2)
                    self.client_sock.close()
                    return

                m = m_format.load(msg)
                if m[m_format.ACTION] == m_format.SEND_MSG:
                    print "%s : %s" % (m[m_format.ID], m[m_format.ACTION_VAL])
                    pass
                elif m[m_format.ACTION] == m_format.BROADCAST:
                    print "BROADCAST : %s" %m[m_format.ACTION_VAL]
                    pass
                elif m[m_format.ACTION] == m_format.SYS_MSG:
                    print "[!!] %s" % m[m_format.ACTION_VAL]
                else:
                    pass

            except Exception as e:
                print (e.message)
                self.client_sock.close()
                return

    def __set_user_info(self):
        id = raw_input("input your name : ")
        self.id = id

    def __connect(self):
        ## set usr id
        ## create or join room
        try:
            self.client_sock.connect(('127.0.0.1', m_format.PORT))

            #### create or join room
            ## recv room info
            print self.client_sock.recv(m_format.BUF_SIZE)

            ## set usr id
            self.__set_user_info()

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
                    return False

            return True

        except Exception as e:
            print (e.message)

    def do(self):
        if self.__connect():
            self.write_thread.start()
            self.read_thread.start()
        else:
            return False

client = Client()
client.do()
