import  socket
import pymysql

def main():
    #创建服务器套接字
    tcp_server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    #端口复用
    tcp_server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,True)
    #绑定端口
    tcp_server_socket.bind(("",9000))
    #设置监听
    tcp_server_socket.listen(128)

    while True:
        # 创建服务器与客户端套接字
        new_socket,ip_port=tcp_server_socket.accept()
        #接受数据
        revc_data=new_socket.recv(4096)
        #接收后判断是否下线
        if(len(revc_data)==0):
            print("浏览器关闭了")
            new_socket.close()
            return
        #接收数据解码
        revc_content=revc_data.decode("utf-8")
        print(revc_content)
        #判断请求是否根目录，返回首页
        # revc_list=revc_content.split(" ",maxsplit=2)
        # print(revc_list[1])
        # if(revc_list[1]=="/"):
        url="static/index.html"

        try:
            #打开指定路径文件，读取指定文件数据
            with  open(url,"rb") as file:
                file_data =file.read()
        except Exception as e:
            #找不到文件时发送404响应报文数据
            response_line="HTTP:/1.1 404 Not Found\r\n"
            response_header="Server:PWS1.0\r\n"
            with open("static/error.html","rb") as file:
                file_data=file.read()
            response_body=file_data
            response_data=(response_line+response_header+"\r\n").encode("utf-8")+response_body
            new_socket.send(response_data)
        else:
            # 正常发送数据
            response_line="HTTP://1.1 200 OK\r\n"
            response_header="SERVER:PWS1.0 \r\n"
            response_body=file_data
            #组装报文
            response_data=(response_line+response_header+"\r\n").encode("utf-8")+response_body
            new_socket.send(response_data)
        finally:
            # 关闭服务器与客户端套接字
            new_socket.close()

if __name__ =="__main__":
    #main()
    conn=pymysql.connect(host='localhost',port=3306,database="stock_db",user='root',password='mysql',charset='utf8',)
    conn.close()
