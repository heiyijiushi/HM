#1.接受文本服务器的动态资源请求
#2.处理动态资源请求并把处理结果返回给web服务器
#3.web服务器把处理结果组装成响应报文发送给浏览器


import time
#首页数据
def index():
    status="200 OK"
    response_header=[("server","PWS2.0")]
    data=time.ctime()
    return  status,response_header,data

#没有找到动态资源
def not_found():
    status="404 Not Found"
    response_header=[("Server","PWS2.0")]
    data="not found"
    return status, response_header, data

def handle_request(env):
    request_path=env["request_path"]
    print("接受后的资源请求",request_path)
    if request_path=="/index.html":
        result=index()
        return result
    else:
        result=not_found()
        return result
