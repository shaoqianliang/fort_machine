from django.test import TestCase

# Create your tests here.
#FTP文件传输
#目录
"""
——FTP
|
|——ftpclinet #ftp客户端
|     |—— __init__.py
|      |_  FtpClinet.py
|
|___ftpserver  #ftp服务端
            ├── README.txt
            ├── ftpserver.py #服务端入口程序
            ├── conf #配置文件目录
            │   ├── __init__.py
            │   └── setting.py
            ├── modules #程序核心目录
            │   ├── __init__.py
            │   ├── auth_user.py  #用户认证模块
            │   └── sokect_server.py  #sokectserver模块
            ├── database #用户数据库
            │   ├── alex.db
            │   ├── lzl.db
            │   └── eric.db
            ├── home #用户宿主目录
            │   ├── alex
            │   ├── lzl
            │   └── eric
            └── log
                ├── __init__.py
                └── log  #待扩展....

"""






import socketserver,socket
import struct,json
import os
# class FtpServer():
#     max_packet_size = 2418
#     server_dir = os.path.dirname(os.path.abspath(__file__))
#     def __init__(self,addr_port):
#         self.server_addr = addr_port
#         self.socket = socket.socket(family=socket.AF_INET,type=socket.SOCK_STREAM)
#         self.socket.bind(self.server_addr)
#         self.socket.listen(5)
#
#     def run(self):
#         while True:
#             self.sock,self.addr = self.socket.accept()
#             while True:
#                 head_stuct =self.sock.recv(4) #通过struct压缩成4个字节
#                 if head_stuct:
#                     head_len = struct.unpack('i',head_stuct)[0] #解压后
#                     head_json = self.sock.recv(head_len).decode('utf-8')
#                     head_dic = json.loads(head_json)
#                     #head_dic {'cmd':'put','filename': 'xiaoshui','size':'7mb'}
#                     cmd = head_dic['cmd']
#                     if hasattr(self,cmd):
#                         func = getattr(self,cmd)
#                         func(head_dic)
#
#     def get(self):#下载
#         pass
#
#     def put(self, args):
#         import os
#         file_path = os.path.normpath(os.path.join(
#             self.server_dir,
#             args['filename']
#         ))
#
#         filesize = args['filesize']
#         recv_size = 0
#         print('----->', file_path)
#         with open(file_path, 'wb') as f:
#             while recv_size < filesize:
#                 recv_data = self.sock.recv(self.max_packet_size)
#                 f.write(recv_data)
#                 recv_size += len(recv_data)
#                 print('recvsize:%s filesize:%s' % (recv_size, filesize))

# if __name__ == '__main':
#     Ftp = FtpServer(('127.0.0.1',8000))
#     Ftp.run()


"""  #socketserver是python标准库的服务框架，封装了socket
import socketserver
import struct
import json
import os
class FtpServer(socketserver.BaseRequestHandler):
    coding='utf-8'
    server_dir='file_upload'
    max_packet_size=1024
    BASE_DIR=os.path.dirname(os.path.abspath(__file__))
    def handle(self):
        print(self.request)
        while True:
            data=self.request.recv(4)
            data_len=struct.unpack('i',data)[0]
            head_json=self.request.recv(data_len).decode(self.coding)
            head_dic=json.loads(head_json)
            # print(head_dic)
            cmd=head_dic['cmd']
            if hasattr(self,cmd):
                func=getattr(self,cmd)
                func(head_dic)
    def put(self,args):
        file_path = os.path.normpath(os.path.join(
            self.BASE_DIR,
            self.server_dir,
            args['filename']
        ))

        filesize = args['filesize']
        recv_size = 0
        print('----->', file_path)
        with open(file_path, 'wb') as f:
            while recv_size < filesize:
                recv_data = self.request.recv(self.max_packet_size)
                f.write(recv_data)
                recv_size += len(recv_data)
                print('recvsize:%s filesize:%s' % (recv_size, filesize))


ftpserver=socketserver.ThreadingTCPServer(('127.0.0.1',8080),FtpServer)
ftpserver.serve_forever()

FtpServer
"""

# import os
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fort_machine.settings")
# import django
# django.setup()
# from audit import models
# print(models.User.objects.filter(pk=1)) #primary key主键


# from wsgiref.simple_server import make_server
# from io import StringIO
# def application(environ,start_response):
#     stdout = StringIO() #读取到内存
#     print("Hello world!", file=stdout)
#     start_response("200 OK", [('Content-Type','text/plain; charset=utf-8')])
#     return [stdout.getvalue().encode('utf-8')] #必须以列表形式返回
# server = make_server('127.0.0.1',8000,application)
# server.serve_forever()


# import socket
# sock = socket.socket()
# sock.bind(('127.0.0.1',8000))
# sock.listen(5)
# while True:
#     print('server running')
#     conn ,addr = sock.accept()
#     data = conn.recv(1024)
#     conn.send(b'HTTP://1.1 200 OK\r\n\r\n<p><strong>hello world</strong></p>')
#     conn.close()

