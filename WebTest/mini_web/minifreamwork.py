import time
import pymysql
import json

#获取首页数据,读取模板，对模板变量进行替换

# route_list = [
#     # 路由列表
#     ("/index.html": index),
#     # ("/center.html":center),
#     ("/error.html": error)
# ]
route_list=[]

#带参数的装饰器
def route(path):
    def decorator(func):
        route_list.append((path,func))
        def inner():
            return func()
        return inner
    return decorator


#处理动态资源请求
def handle_request(env):



    request_path=env["request_path"]
    print("接收到的动态资源请求",request_path)


    for path,func in route_list:
        print("路径",route_list)

        if(request_path==path):
            print("找到路径了", request_path)
            result=func()
            return result
    else:
        # 没有找到动态资源
        result = not_found()
        return result

    # if(request_path=="/index.html"):
    #     # 首页数据
    #     result=index()
    #     return result
    # else if(request_path="/center.html"):
    #     result=center()
    #     return center()
    # else:
    #     # 没有找到动态资源
    #     result=not_found()
    #     return result

#获取首页数据
@route("/index.html")
def index():
    #响应状态
    status="HTTP/1.1 200 OK \r\n"
    #响应头
    response_header=["Server","PWS2.0"]
    #打开模板
    with open("Template/index.html", "r") as file:
        file_data=file.read()

    #处理后的数据，从数据库种查询，暂时用时间替代
    #data=time.ctime()

    #数据库处理
    conn=pymysql.connect(host='localhost',port=3306,user="root",password="mysql",database='stock_db',charset='utf8')
    cursor= conn.cursor()
    sql="select * from info;"
    cursor.execute(sql)
    result=cursor.fetchall()
    print('数据库查询结果：',result)
    # #
    data=""
    for row in result:
        data+='''<tr>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td><input type="button",id="toadd",text="添加",name="toAdd"></td>
        </tr>'''%row
    result2=file_data.replace("{%content%}",data)
    return  status,response_header,result2



#提供JSON接口
@route("/center.html")
def center_data():
    status="HTTP/1.1 200 OK"
    response_header=[("Server","PWS2.0"),("Content-Type","text/html,charset=utf-8")]
    conn=pymysql.connect(host="localhost",database="stock_db",user="root",password="mysql")
    cursor=conn.cursor()
    sql='''
    select i.code,i.short,i.chg,i.turnover,i.price,i.highs,f.note_info
    from info as i inner join focus as f on i.id=f.info_id;
    '''
    cursor.execute(sql)
    result=cursor.fetchall()
    cursor.close()

    center_data_list=list()

    for row in result:
        conter_dict=dict()
        conter_dict["code"]=row[0]
        conter_dict["short"]=row[1]
        conter_dict["chg"]=row[2]
        conter_dict["turnover"]=row[3]
        conter_dict["price"]=str(row[4])
        center_data_list.append(conter_dict)

    json_str=json.dumps(center_data_list,ensure_ascii=False)
    print(json_str)
    return status,response_header,json_str


#没有找到动态资源
@route("/error.html")
def not_found():
    #响应状态
    status="HTTP/1.1 404 Not Found \r\n"
    #响应头
    response_header=["Server","PWS2.0"]
    #打开模板


    #处理后的数据，从数据库种查询，暂时用时间替代
    data="动态资源 not found%s"

    return  status,response_header,data

@route("/Data.html")
def data():
    status="HTTP/1.1 200 OK \r\n"
    response_header=[("Server","PWS2.0")]
    with open ("Data.html", "rb") as file:
        file_data=file.read()
    # conn=pymysql.connect(host="localhost",database="stock_db",user="root",password="mysql",charset="utf8")
    # cursor=conn.cursor()
    # sql="select code,chg,price,short from info;"
    # cursor.execute(sql)
    # result=cursor.fetchall()
    # cursor.close()
    # conn.close()
    # result_list=list()
    # for row in result:
    #     data_dict=dict()
    #     data_dict["code"]=str(row[0])
    #     data_dict["Chg"]=row[1]
    #     data_dict["price"] = str(row[2])
    #     data_dict["short"] = row[3]
    #     result_list.append(data_dict)

    response_body = (file_data.decode("utf-8")).replace("{%centerData%}", "")
    print(response_body)
    # json_result=json.dumps(result_list,ensure_ascii=False)
    #
    # return status,response_header,json_result
    return    status, response_header,response_body
# 获取个人中心数据
@route("/center_data.html")
def center_data():
    # 状态信息
    status = "200 OK"
    # 响应头信息
    response_header = [("Server", "PWS/1.1")]
    # 1. 打开指定模板文件，读取模板文件中的数据
    with open("Data.html", "rb") as file:
        file_data = file.read()
    # 2. 查询数据库，模板里面的模板变量( {%content%}) 替换成以后从数据库里面查询的数据

    response_body = (file_data.decode("utf-8")).replace("{%centerData%}", "")
    print(response_body)
    # 这里返回的是元组
    return status, response_header, response_body

