#coding=utf8
'''
name;levi
time;2018-10-1
'''

from socket import *
import sys
import re
from threading import Thread
import time
from seting import *


class HTTPServer(object):
    def __init__(self,addr=('0.0.0.0',80)):
        self.sockfd=socket()
        self.sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
        self.addr=addr
        self.bind(addr)

    def bind(self,addr):
        self.ip=addr[0]
        self.port=addr[1]
        self.sockfd.bind(addr)
    #http服务器启动
    def serve_forever(self):
        self.sockfd.listen(10)
        print('listen the port %d'%self.port)
        while True:
            connfd,addr=self.sockfd.accept()
            print('connect from',addr)
            handle_client=Thread(target=self.handle_request,args=(connfd,))
            handle_client.setDaemon(True)
            handle_client.start()

    def handle_request(self,connfd):
        #接受浏览器请求
        request=connfd.recv(4096)
        # print(request)
        request_lines=request.splitlines()
        #获取请求行
        request_line=request_lines[0].decode()
        #正则表达式提取请求方法和内容
        pattern=r'(?P<METHOD>[A-Z]+)\s+(?P<PATH>/\S*)'
        try:
            env=re.match(pattern,request_line).groupdict()
        except:
            response_headlers='HTTP/1.1 500 server error\r\n'
            response_headlers+='\r\n'
            response_body='server error'
            response=response_headlers+response_body
            connfd.send(response.encode())
            return
    #将请求发送给frame得到返回数据结果
        status,response_body=self.send_request(env['METHOD'],env['PATH'])
    #根据响应吗组织响应头内容
        response_headlers=self.get_headlers(status)
    #将结果组织为httpresponse发送给客户端    
        response=response_headlers+response_body
        connfd.send(response.encode())
        connfd.close()
    #和frame交互发送request获取response
    def send_request(self,method,path):
        s=socket()
        s.connect(frame_addr)
        #向webframe发送method /path
        s.send(method.encode())
        time.sleep(0.1)
        s.send(path.encode())

        status=s.recv(128).decode()
        response_body=s.recv(4096*10).decode()
        return status,response_body


    def get_headlers(self,status):
        if status=='200':
            response_headlers='HTTP/1.1 200 OK\r\n'
            response_headlers+='\r\n'
        elif status=='400':
            response_headlers='HTTP/1.1 404 NOT FOUND\r\n'
            response_headlers+='\r\n'

        return response_headlers

if __name__=='__main__':
    httpd=HTTPServer(ADDR)

    #启动服务器
    httpd.serve_forever()






















