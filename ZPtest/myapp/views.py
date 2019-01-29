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
    user_name_phone_email = request.POST.get('user_name')
    pwd = request.POST.get('user_pwd')
    users_name_login = Users.objects.filter(login_name=user_name_phone_email, login_pwd=pwd)
    users_phone_login = Users.objects.filter(user_phone=user_name_phone_email, login_pwd=pwd)
    users_email_login = Users.objects.filter(user_email=user_name_phone_email, login_pwd=pwd)
    if users_name_login or users_phone_login or users_email_login:
        if users_name_login:
            user = users_name_login.first()
            request.session['user_id'] = user.id
        if users_phone_login:
            user.id = users_phone_login.first()
            request.session['user_id'] = user.id
        if users_email_login:
            user.id = users_email_login.first()
            request.session['user_id'] = user.id
        return redirect(reverse('NB:go_user_mine'))
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
    login_name_phone_email = request.POST.get('username')  # 用户名或者电话
    login_pwd = request.POST.get('password')  # 密码
    company_name_login = Companies.objects.filter(login_name=login_name_phone_email, login_pwd=login_pwd)  # 实例化表对象
    company_phone_login = Companies.objects.filter(company_phone=login_name_phone_email, login_pwd=login_pwd)
    company_email_login = Companies.objects.filter(company_email=login_name_phone_email, login_pwd=login_pwd)
    if company_name_login or company_phone_login or company_email_login:  # 预留session
        if company_name_login:
            company = company_name_login.first()
            request.session['company_id'] = company.id
        if company_phone_login:
            company = company_name_login.first()
            request.session['company_id'] = company.id
        if company_email_login:
            company = company_email_login.first()
            request.session['company_id'] = company.id
        return redirect(reverse('NB:go_company_mine'))
    else:
        return redirect(reverse('NB:company_home'))


def go_user_reset(request):
    if request.session.get('user_id'):
        return render(request, 'user_reset.html')
    else:
        return render(request, 'user_login.html')


def go_company_reset(request):
    if request.session.get('company_id'):
        return render(request, 'company_reset.html')
    else:
        return render(request, 'company_login.html')


def go_company_mine(request):
    if request.session.get('company_id'):
        return render(request, 'company_mine.html')
    else:
        return redirect(reverse('NB:company_home'))


def go_user_mine(request):
    if request.session.get('user_id'):
        return render(request, 'user_mine.html')
    else:
        return redirect(reverse('NB:user_home'))


def go_company_zhiweisousuo(request):
    if request.session.get('company_id'):
        return render(request, 'company_zhiweilist.html')
    else:
        return render(request, 'company_login.html')


def go_cpmpany_shoujianxiang(request):
    if request.session.get('company_id'):
        return render(request, 'company_shoujianxiang.html')
    else:
        return render(request, 'company_login.html')


def go_user_vip(request):
    if request.session.get('user_id'):
        return render(request, 'user_vip.html')
    else:
        return render(request, 'user_login.html')


def go_company_vip(request):
    if request.session.get('company_id'):
        return render(request, 'company_vip.html')
    else:
        return render(request, 'company_login.html')


def go_company_recaija(request):
    if request.session.get('company_id'):
        return render(request, 'company_rencaijia.html')
    else:
        return render(request, 'company_login.html')


def upload_resume_home(request):  # 上传简历
    if request.session.get('user_id'):
        return render(request, 'upload_resume.html')
    else:
        return render(request, 'user_login.html')


def upload_job_home(request):  # 岗位发布
    if request.session.get('company_id'):
        return render(request, 'upload_job.html')
    else:
        return render(request, 'company_login.html')


def zwss_home(request):  # 职位搜索
    if request.session.get('user_id'):
        return render(request, 'zhiweisousuo.html')
    else:
        return render(request, 'user_login.html')


def save_xinxi(request):
    if request.session.get('user_id'):
        users = request.POST
        user_name = users['user_name']
        sex = users['sex']
        age = users['']
        res = {'status': 200}
        return JsonResponse(res)
    else:
        return render(request, 'user_login.html')


def save_job(request):
    pass


def email_phone_set(request):  # 查看数据库中是否存在该邮箱和电话
    data = {}
    phone = request.GET.get('phone')
    email = request.GET.get('email')
    user = request.GET.get('user')
    if user == 'user':
        if Users.objects.filter(user_email=email, user_phone=phone):
            data['status'] = 200
            print(data)
            return JsonResponse(data)
        else:
            data['status'] = 404
            print(data)
            return JsonResponse(data)
    else:
        if Companies.objects.filter(company_phone=phone, company_email=email):
            data['status'] = 200
            print(data)
            return JsonResponse(data)
        else:
            data['status'] = 404
            print(data)
            return JsonResponse(data)


def email_phone_reset(request):
    data = {}
    user = request.GET.get('user')
    phone = request.GET.get('phone')
    email = request.GET.get('email')
    if user == 'user':
        user_company = Users.objects.filter(user_phone=phone, user_email=email)
    else:
        user_company = Companies.objects.filter(company_phone=phone, company_email=email)

    pwd = user_company[0].login_pwd
    name = user_company[0].login_name
    try:
        text = '账号：{} 密码：{}'.format(name, pwd)
        mail(your_user=email, content_text=text)
        data['status'] = 200
        data['show'] = '邮箱发送成功，请查收'
        return JsonResponse(data)
    except Exception as e:
        print(e)
        data['status'] = 404
        data['status'] = '发送失败'
        return JsonResponse(data)


def set_phone(request):
    data = {}
    phone = request.GET.get('phone')
    user = request.GET.get('user')
    if user == 'user':
        if Users.objects.filter(user_phone=phone):
            data['status'] = 200
            data['title'] = '改手机号已经被注册过'
            return JsonResponse(data)
        else:
            data['status'] = 404
            return JsonResponse(data)
    else:
        if Companies.objects.filter(company_phone=phone):
            data['status'] = 200
            data['title'] = '改手机号已经被注册过'
            return JsonResponse(data)
        else:
            data['status'] = 404
            return JsonResponse(data)


def set_email(request):
    data = {}
    email = request.GET.get('email')
    user = request.GET.get('user')
    if user == 'user':
        if Users.objects.filter(user_email=email):
            data['status'] = 200
            data['title'] = '该邮箱已经被注册过'
            print(data)
            return JsonResponse(data)
        else:
            data['status'] = 404
            return JsonResponse(data)
    else:
        if Companies.objects.filter(company_phone=email):
            data['status'] = 200
            data['title'] = '改邮箱已经被注册过'
            return JsonResponse(data)
        else:
            data['status'] = 404
            return JsonResponse(data)
