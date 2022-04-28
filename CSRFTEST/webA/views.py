from django.shortcuts import render,redirect
from django.views import View
from django.http import HttpResponse,HttpRequest
from django.shortcuts import reverse
from django.middleware.csrf import  get_token
# Create your views here.

class LoginView(View):

    def __init__(self):
        print("进入login")
        print(View.http_method_names)

    def get(self,request):
        print("这是get方法")
        return render (request,'webA/login.html')
    def post(self,request):
        print("post方法")
        username = request.POST.get("username")
        password=request.POST.get("password")

        if not all([username,password]):
            print("参数错误")
        else:
            print(username,password)
            if(username=='zhangsan' and password=='321'):
                response=redirect(reverse('transfer'))
                response.set_cookie("username",username)
                return response
            else:
                print("密码错误")
        print("退出Login")

        return HttpResponse("OK")


class TransferView(View):
    def __init__(self):
        print("进入Transfer")


    def post(self,request):

        print("这是Transfer的post方法")
        from_csrf_token=request.POST.get('csrftoken')
        cookie_csrf_token=request.COOKIES.get('csrf_token')
        if cookie_csrf_token!=from_csrf_token:
            return HttpResponse("toke校验失败，非法操作")
        username=request.COOKIES.get('username',None)
        if not username:
            print("没有匹配用户名哦")
            return redirect(reverse('index'))
        to_account=request.POST.get('to_account')
        money=request.POST.get("money")
        print("执行转账")
        return HttpResponse("转账%s元到%s成功"%(money,to_account))


    def get(self,request):
        print("这是Transfer的get方法")
        csrf_token=get_token(request)

        username = request.COOKIES.get('username', None)
        print("cookie的用户名是%s"% username)

        response= render(request,'webA/transfer.html',context={'csrf_token':csrf_token})

        response.set_cookie('csrf_token',csrf_token) #设置csrf_token到cookie
        return response
