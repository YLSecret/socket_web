#!/usr/bin/python

import socket, re, sys
from threading import Thread
import application

class HttpServer(object):
    def __init__(self):
        tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tcp_server_socket.bind(('192.168.40.134', 7890))
        tcp_server_socket.listen(128)
        self.tcp_server_socket = tcp_server_socket

    def start(self):
        while True:
            new_client_socket, ip_port = self.tcp_server_socket.accept()
            print("新客户端来了", ip_port)
            # 处理函数
            # request_handler(new_client_socket)
            # 线程处理
            t1 = Thread(target=self.request_handler, args=(new_client_socket,))
            t1.start()

    def request_handler(self, new_client_socket):
        recv_data = new_client_socket.recv(1024)
        if not recv_data:
            print("客户端断开连接")
            new_client_socket.close()
            return
        recv_text = recv_data.decode()
        ret_list = recv_text.split('\r\n')
        ret = re.search("\s(.*)\s", ret_list[0])
        if ret == '':
            print("请求路径不正确")
            new_client_socket.close()
            return
        request_path = ret.group(1)
        print('请求路径:',request_path)
        if request_path == "/":
            request_path = "/index.html"
        # 判端动态资源请求
        if request_path.endswith(".html"):
            evn = {
                "path_info":request_path
            }
            # 框架包
            status, heads, response_body = application.app(evn)
            response_line = "HTTP/1.1 %s\r\n"%status
            response_head = ''
            for head in heads:
                response_head = "%s:%s\r\n"%head

            response_data = (response_line + response_head + "\r\n" + response_body).encode()
            new_client_socket.send(response_data)
            new_client_socket.close()

        # 静态资源请求
        else:
            # 拼接响应报文
            response_head = "Server:pythonBWs/1.1\r\n"
            response_blank = "\r\n"
            response_body = ''
            response_line = ''
            try:
                with open("static" + request_path, 'rb') as file:
                    response_body = file.read()
            except Exception as e:
                response_line = "HTTP/1.1 404 NOT Found\r\n"
                response_body = "Error:%s\r\n" % e

            else:
                response_line = "HTTP/1.1 200 OK\r\n"
            finally:
                response_data = (response_line + response_head + response_blank).encode() + response_body
                new_client_socket.send(response_data)
                new_client_socket.close()


def main():

    # if len(sys.argv) != 2:
    #     print("请输入正确的参数 例如:python3 ***.py 7890")
    #     return
    #
    # if not sys.argv[1].isdigit():
    #     print('端口号必须为纯数字')
    #     return
    # port = int(sys.argv[1])
    httpserver = HttpServer()
    httpserver.start()


if __name__ == '__main__':
    main()
