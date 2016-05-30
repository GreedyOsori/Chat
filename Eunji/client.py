# -*- coding:utf-8 -*-
import socket
import sys

HOST = '127.0.0.1'
PORT = 3223


if __name__ == '__main__':
    #name = raw_input('Client name: ')
    #소켓 생성
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #연결 요청
    sock.connect((HOST, PORT))
    print 'Client connected to server. Please Type something'

    while 1:
        # 키보드 입력 처리
        message = raw_input()
        sock.send(message)

        #종료 처리
        if (message == "quit"):
            sock.close()
            sys.exit()

        #Now receive data
        received = sock.recv(4096)
        print received