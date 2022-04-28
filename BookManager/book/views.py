from django.shortcuts import render
from django.http import HttpResponse
from . import models
from django.views.generic import View
# Create your views here.

def index(request):
    context={'title':"模板TEST"}
    #return HttpResponse("HelloWorld{}".format(request.path))
    return  render(request,"book/index.html",context)

def booklist(request):

    #查询数据库书籍列表
    books=models.BookInfo.objects.all()
    print("书籍列表：",books)
    context={'books':books}
    #数据交给模板处理，处理完成后通过视图响应给客户端
    return render(request,'book/booklist.html',{'booklist':books})


def test(request,num2,num1):
    print('进来了1')
    print(num1," ",num2)
    return HttpResponse("ok")

def test2(request,num2,num1):
    print('进来了2')
    print(num1," ",num2)
    return HttpResponse("ok")

def test3(request,num1):
    print('进来了3')
    print(num1)
    return HttpResponse("ok")


def register(request):
    """处理注册"""

    # 获取请求方法，判断是GET/POST请求
    if request.method == 'GET':
        # 处理GET请求，返回注册页面
        return render(request, 'register.html')
    else:
        # 处理POST请求，实现注册逻辑
        return HttpResponse('这里实现注册逻辑')

#类视图
class Register(View):
    def get(self,request):
        print("这个是get方法")
        return HttpResponse("get方法")
    def post(self):
        print("Post方法")
        return HttpResponse("Post方法")

def middleware(request):
    print('view 视图被调用')
    return HttpResponse('OK')
