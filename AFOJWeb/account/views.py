#coding=utf-8
import re
from django.db import IntegrityError
from django.contrib.auth.models import User
from account.models import UserOJ,Privilege
from django.shortcuts import render
from django.shortcuts import render_to_response,RequestContext
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
# Create your views here.
# def login(request):
#     return render_to_response( "account/login.html",RequestContext(request,{}))

def sign_up(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        studentId = request.POST.get('school_ID', '')
        password = request.POST.get('password', '')
        
        if not re.match(ur'[a-zA-Z0-9_\u4e00-\u9fa5]{2,20}$', unicode(username)):
            return render(request, "account/sign_up.html",
                    {"error": '格式有误'})

        if not re.match(ur'[0-9]{9,11}', unicode(studentId)):

            error = '学号格式有误'
            return render(request, "account/sign_up.html", {'error': error})

        if not re.match(ur'[\w!#$%&*+/=?^_`{|}~-]+(?:\.[\w!#$%&*+/=?^_`{|}~-]+)*@(?:[\w](?:[\w-]*[\w])?\.)+[\w](?:[\w-]*[\w])?', email):
            error = '邮箱格式不对'
            return render(request, "account/sign_up.html", {'error': error})

        if not re.match(ur'.{3,20}', password):
            error = '看看你密码的格式哦，不能少于3个字符'
            return render(request, "account/sign_up.html", {'error': error})
        try:
            user=UserOJ.objects.get(studentId=str(studentId))
            error = '你的学号好像已经有人注册了'
            print error
            return render(request, "account/sign_up.html", {'error': error})
        except:
            print "studentId Aviable"

        try:
            user = User.objects.create_user(username=username,
                             password=password, email=email)
        except IntegrityError:
            error = '这个用户名已经有人使用了 !'
            return render(request, "account/sign_up.html", {'error' : error})

        UserOJ.objects.create(user=user, studentId=studentId)
        user=authenticate(username=username,password=password)
        login(request,user)
        # return render_to_response("index.html",RequestContext(request,))
        return HttpResponseRedirect("/")
    return render_to_response("account/sign_up.html",RequestContext(request,{}))

# def sign_in(request):
#     print "what happened"
#     if request.method == 'POST':
#         next_url = request.POST.get('next', '/')
#         username = request.POST.get('username', '')
#         password = request.POST.get('password', '')
#         print username+password
#         user = authenticate(username=username, password=password)
#         # print user+"hffdjaljf"
#         if user is not None:
#             if user.is_active:
#                 login(request, user)
#                 return render(request, 'index.html', {
#                     'next_url' : next_url,
#                     'info' : '成功登陆'
#                     })
#             else:
#                 error = '账户停用!'
#                 return render(request, "account/login.html",
#                         {'error' : error, 'next' : next_url})
#         else:
#             error ='你是不是输入错密码了呢？'
#             return render(request, "user/sign_in.html",{'error' : error, 'next' : next_url})
#     next_url = request.GET.get('next', '/')
#     return render(request, "account/login.html", {'next' : next_url})
def sign_in(request):

    if request.method=="POST":
        username=request.POST.get('username','')
        password=request.POST.get('password','')
        user=authenticate(username=username,password=password)
        if user is not None:
            if user.is_active:
                login(request,user)
                info="成功登陆"
                return render_to_response("index.html",RequestContext(request,{"info":info}))
            else:
                 info="用户过期"
                 return render_to_response("account/login.html",RequestContext(request,{"info":info}))
        else:
             info="用户名或者密码错误"
             return render_to_response("account/login.html",RequestContext(request,{"info":info}))
    else:
            info="请输入用户名密码"
            return render_to_response("account/login.html",RequestContext(request,{"info":info}))
@login_required
def log_out(request):
        logout(request)
        return HttpResponseRedirect('/account/')
