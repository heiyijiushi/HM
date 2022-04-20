import socket
import threading
import sys
import freamework

class HttpWebServer(object):
    def __init__(self,port):
        #创建服务端套接字
        tcp_server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        #关闭套接字，端口复用
        tcp_server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,True)
        #绑定端口
        tcp_server_socket.bind(("",port))
        #监听
        tcp_server_socket.listen(128)

        self.tcp_server_socket=tcp_server_socket

    @staticmethod
    def handle_client_request(new_socket):
         recv_client_data=new_socket.recv(4096)
         if len(recv_client_data)==0: #判断通讯终止
             print("浏览器关闭了")
             new_socket.close()
             return
         revc_client_content=recv_client_data.decode("utf-8") #二进制解码
         print(revc_client_content)

         request_list=revc_client_content.split(" ",maxsplit=2)

         request_path=request_list[1]
         print(request_path)

         if request_path.endswith(".html"):
             env={"request_path":request_path}
             #获取框架处理结果
             status,handers,response_body=freamework.handle_request(env)
             print("handers:%s"%handers)
             response_line="HTTP/1.1 %s\r\n" %status
             response_header=""
             for header in handers:
                 response_header+="%s:%s\r\n"%header
             response_data=(response_line+response_header+"\r\n"+response_body).encode("utf-8")
             new_socket.send(response_data)
             new_socket.close()
         else:
            try:
                with open("static"+request_path,"rb") as file:
                    file_data=file.read()
            except Exception as e:
                response_line="HTTP/1.1 404 Not Found \r\n"
                response_header="Server:PWS1.0\r\n"
                with open("static/error.html","rb")as file:
                    file_data=file.read()
                response_body=file_data
                response_data=(response_line+response_header+"\r\n").encode("utf-8")+response_body
                new_socket.send(response_data)
            else:
                response_line="HTTP/1.1 200 OK \r\n"
                response_header="Server PWS1.0 \r\n"
                response_body=file_data
                response_data=(response_line+response_header+"\r\n").encode("utf-8")+response_body
                new_socket.send(response_data)
            finally:
                new_socket.close()

    def start(self):
        while True:
            new_socket,ip_port = self.tcp_server_socket.accept()
            sub_thread=threading.Thread(target=self.handle_client_request,args=(new_socket,),daemon=True)
            sub_thread.start()
def main():
        # if len(sys.argv) != 2:
        #     print("执行名称输入错误 示例 python3 xxx.py 9000")
        #     return
        # if not sys.argv[1].isdigit():
        #     print("执行端口输入错误 示例 python3 xxx.py 9000")
        #     return
        # #端口需要转换为int类型
        # port=int(sys.argv[1])
        #创建web服务器
        web_server=HttpWebServer(4000)
        #启动web服务器
        web_server.start()



if __name__=="__main__":
    main()
