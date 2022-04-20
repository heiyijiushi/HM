#1.导入socket he threading模块
import  socket
import  threading
import time
#2.创建服务器套接字
#3.服务器端口复用
#4.服务器绑定端口
#5.服务器监听
#6.处理客户端请求
#7.接受数据
#8.发送数据（错误404数据和首页）
#9.关闭服务端和客户端套接字

def handle_client_request(new_socket):
    recv_data=new_socket.recv(4096)
    if(len(recv_data)==0):
        print("浏览器关闭了")
        new_socket.close()
        return
    revc_content=recv_data.decode("utf-8")
    print(revc_content)
    request_list=revc_content.split(" ",maxsplit=2)
    print("返回字符串", (request_list))
    request_path=request_list[1]
    print("是否根目录",(request_path))

    if(request_path=="/"):
        request_path="/index.html"

    print("正确", request_path)
    try:
        with open ("static"+request_path,"rb") as file:
            file_data=file.read()
    except Exception as e:
        print("返回错误页面")
        response_line="HTTP:/1.1 404 Not Found\r\n"
        response_header="Server:PWS1.0 \r\n"
        with open("static/error.html","rb") as file:
            file_data=file.read()
        print(file_data)
        response_body=file_data
        response_data=(response_line+response_header+"\r\n").encode("utf-8")+response_body
        new_socket.send(response_data)
    else:
        print("返回首页")
        response_line="HTTP:/1.1 200 OK\r\n"
        response_header="Server:PWS1.0\r\n"
        response_body=file_data
        print(file_data)
        response_data=(response_line+response_header+"\r\n").encode("utf-8")+response_body
        new_socket.send(response_data)
    finally:
        new_socket.close()
def main():
    tcp_server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    tcp_server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,True)
    tcp_server_socket.bind(("",8000))
    tcp_server_socket.listen(128)

    while True:
        new_socket,ip_port=tcp_server_socket.accept()
        print(ip_port)
        sub_thread=threading.Thread(target=handle_client_request,args=(new_socket,),daemon=True)
        sub_thread.start()
    time.sleep(0.2)
    # tcp_server_socket.close()


if __name__=="__main__":
    main()


'''
 1.客户端和服务端建立连接成功，创建子线程，使用子线程专门处理客户端请求，防止主线程堵塞
 2.创建的主线程设置成守护主线程，防止主线程无法退出
 3.可以同时处理多个客户端的请求，更加节省内存资源

'''

