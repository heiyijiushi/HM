import socket
import  threading
import sys

class HttpWebServer(object):
    def __init__(self,port):
        tcp_server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        tcp_server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,True)
        tcp_server_socket.bind(("",port))
        tcp_server_socket.listen(128)
        self.tcp_server_socket=tcp_server_socket

    @staticmethod
    def handle_client_request(new_socket):
        recv_client_data = new_socket.recv(4096)
        if(len(recv_client_data)==0):
            print("浏览器关闭了")
            new_socket.close()
            return
        recv_client_content=recv_client_data.decode("utf-8")
        request_list=recv_client_content.split(" ",maxsplit=2)
        if(request_list[1]=="/"):
            request_path="/index.html"
        try:
            with open("static"+request_path,"rb") as file:
                file_data=file.read()
        except Exception as e:
            response_line="HTTP 1.1 400 Not Found \r\n"
            response_header="Server PWS1.0\r\n"
            with open("static/error.html","rb") as file:
                file_data=file.read()
            response_body=file_data
            response_data=(response_line+response_header+"\r\n").encode("utf-8")+response_body
            new_socket.send(response_data)
        else:
            response_line="HTTP 1.1 200 OK \r\n"
            response_header="Server PWS1.0\r\n"
            response_body=file_data
            response_data =(response_line + response_header + "\r\n").encode("utf-8") + response_body
            new_socket.send(response_data)
        finally:
            new_socket.close()

    #启动Web服务器
    def start(self):
        while True:
            new_socket, ip_port = self.tcp_server_socket.accept()
            sub_thread = threading.Thread(target=self.handle_client_request, args=(new_socket,), daemon=True)
            sub_thread.start()


def main():


    print("主方法")
    #获取python程序的终端命令行程序
    print(sys.argv)
    if len(sys.argv)!=2 or not sys.argv[1].isdigit():
        print("启动命令行如下 python3 xxx.py 8000")
        return
    else:
        print("端口号为：",sys.argv[1],"正在启动多线程web服务器")
        web_server=HttpWebServer(int(sys.argv[1]))
        #启动
        web_server.start()


if __name__=="__main__":
    main()