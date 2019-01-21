
from django.shortcuts import redirect, render
from django.urls import reverse

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
    login_name = request.POST.get('username')
    login_pwd = request.POST.get('userpwd')
    user_phone = request.POST.get('phone')
    user_email = request.POST.get('email')
    new_user = User()
    new_user.login_name = login_name
    new_user.login_pwd = login_pwd
    new_user.user_phone = user_phone
    new_user.user_email = user_email
    new_user.save()
    return redirect(reverse('NB:user_home'))


def user_login(request):
    name = request.POST.get('login_name')
    pwd = request.POST.get('login_pwd')
    users = User.objects.filter(login_name=name, login_pwd=pwd)
    if users:
        user = users.first()
        #登陆成功后设置session属性，预留
        return redirect(reverse('NB:use'))
    else:
        return redirect(reverse('NB:user_home'))


def company_register(request):
    """
     login_pwd :预留md5加密
    """
    login_name = request.POST.get('login_name')
    login_pwd = request.POST.get('login_pwd')
    company_name = request.POST.get('company_name')
    company_email = request.POST.get('company_email')
    company_phone = request.POST.get('company_phone')
    company_info = request.POST.get('company_info')
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
    company_name_phone = request.POST.get('')  # 用户名或者电话
    company_pwd = request.POST.get('')  # 密码
    company = Companies.objects.filter(company_name=company_name_phone, company_pwd=company_pwd)  # 实例化表对象
    if company:  # 预留session
        return redirect(reverse('NB:company'))
    else:
        return redirect(reverse('NB:company_home'))



