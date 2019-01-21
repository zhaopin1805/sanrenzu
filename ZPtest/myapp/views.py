from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from email_demo import mail
from myapp.models import *


def user_home(request):
    return render(request, 'user_login.html')


def company_home(request):
    return render(request, 'company_login.html')


def user_register_home(request):
    return render(request, 'user_regrster.html')


def company_register_home(request):
    return render(request, 'company_regrster.html')


def user_register(request):
    login_name = request.POST.get('user_name')
    login_pwd = request.POST.get('user_pwd')
    user_phone = request.POST.get('phone')
    user_email = request.POST.get('email')
    new_user = Users()
    new_user.login_name = login_name
    new_user.login_pwd = login_pwd
    new_user.user_phone = user_phone
    new_user.user_email = user_email
    new_user.save()
    return redirect(reverse('NB:user_home'))


def user_login(request):
    name = request.POST.get('login_name')
    pwd = request.POST.get('login_pwd')
    users = Users.objects.filter(login_name=name, login_pwd=pwd)
    if users:
        user = users.first()
        # 登陆成功后设置session属性，预留
        return redirect(reverse('NB:use'))
    else:
        return redirect(reverse('NB:user_home'))


def company_register(request):
    """
     login_pwd :预留md5加密
    """
    login_name = request.POST.get('company_name')
    login_pwd = request.POST.get('company_pwd')
    company_name = request.POST.get('name')
    company_email = request.POST.get('company_email')
    company_phone = request.POST.get('company_phone')
    company_info = request.POST.get('com_info')
    company = Companies()  # 实例化表对象
    company.login_name = login_name
    company.login_pwd = login_pwd
    company.company_name = company_name
    company.company_email = company_email
    company.company_phone = company_phone
    company.company_info = company_info
    company.save()
    return redirect(reverse('NB:company_home'))


def company_login(request):
    login_name_phone = request.POST.get('username')  # 用户名或者电话
    login_pwd = request.POST.get('password')  # 密码
    company_name_login = Companies.objects.filter(login_name=login_name_phone, login_pwd=login_pwd)  # 实例化表对象
    company_phone_login = Companies.objects.filter(company_phone=login_name_phone, login_pwd=login_pwd)
    if company_name_login or company_phone_login:  # 预留session
        return redirect(reverse('NB:company'))
    else:
        return redirect(reverse('NB:company_home'))


def go_user_reset(request):
    return render(request, 'user_reset.html')


def user_set(request):  # 查看数据库中是否存在该邮箱和电话
    data = {}
    phone = request.GET.get('phone')
    email = request.GET.get('email')
    print(phone,email)
    if Users.objects.filter(user_email=email, user_phone=phone):
        data['status'] = '200'
        print(data)
        return JsonResponse(data)
    else:
        data['status'] = '404'
        print(data)
        return JsonResponse(data)


def user_reset(request):
    phone = request.POST.get('phone')
    email = request.POST.get('email')
    user = Users.objects.filter(user_phone=phone,user_email=email)
    pwd = user.login_pwd
    name = user.login_name
    text = '账号：{} 密码：{}'.format(name,pwd)
    mail(user=email,title_text=text)