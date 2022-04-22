from django.shortcuts import render
from django.http import HttpResponse
from . import models
# Create your views here.

def index(request):
    context={'title':"模板TEST"}
    #return HttpResponse("HelloWorld{}".format(request.path))
    return  render(request,"book/index.html",context)

def booklist(request):
    #查询数据库书籍列表
    books=models.BookInfo.objects.all()
    context={'books':books}
    #数据交给模板处理，处理完成后通过视图响应给客户端
    return render(request,'book/booklist.html',context)
