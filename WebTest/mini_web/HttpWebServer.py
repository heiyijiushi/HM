import socket
import threading
import minifreamwork

class HttpWebServer(object):

    #方法1：初始化套接字
    def __init__(self,port):
        server_socket= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,True)
        server_socket.bind(("",port))
        server_socket.listen(128)

        self.server_socket=server_socket

    #方法2：处理客户端请求和连接接
    @staticmethod
    def request_handle(recv_socket):
        #链接成功后往下执行
        recv_data=recv_socket.recv(4096)
        if(len(recv_data)==0):
            print("浏览器关闭了")
            recv_socket.close()
            return

        recv_content=recv_data.decode("utf-8")
        print("返回访问数据",recv_content)
        request_list=recv_content.split(" ",maxsplit=2)
        request_path=request_list[1]
        print("分析:",request_path)

        # #判断路径，映射访问关系
        # if(request_path=="/"):
        #
        #     request_path="static/index.html"
        #判断是否动态资源请求，无后缀时为静态资源请求
        if(request_path.endswith(".html")):

            env={
                "request_path":request_path
            }
            status,response_headers,response_body=minifreamwork.handle_request(env)

            response_line=status
            response_header=""
            #拼接文件头
            for header in response_headers:
                response_header+="%s:%s \r\n"%header
                print(header)
            print("文件头：",response_header)

            response_data=(response_line+response_header+"\r\n"+response_body).encode("utf-8")
            recv_socket.send(response_data)
            recv_socket.close()
        #静态资源请求
        else:
            try:
                print("打开静态资源:"%request_path)
                with open(request_path,"r")  as file:
                    file_data=file.read()
            except Exception as e:
                print("没有找到文件",e)
                response_line="HTTP/1.1 404 Not Found\r\n"
                response_head="Server: PWS1.0\r\n"
                with open("static/error.html","rb")  as file:
                    file_data = file.read()
                response_body=file_data
                print("读取文件%s"%response_body)
                response_data=(response_line+response_head+"\r\n").encode("utf-8")+response_body
                recv_socket.send(response_data)
            else:
                response_line = "HTTP /1.1 200 OK\r\n"
                response_head = "Server: PWS1.0\r\n"
                response_body = file_data
                response_data = (response_line + response_head + "\r\n").encode("utf-8") + response_body
                recv_socket.send(response_data)
            finally:
                recv_socket.close()



    #方法3：启动方法
    def start(self):
        while True:
            new_socket,ip_port=self.server_socket.accept()
            print("上线了", ip_port)
            socket_threading=threading.Thread(target=self.request_handle,args=(new_socket,),daemon=True)
            socket_threading.start()





