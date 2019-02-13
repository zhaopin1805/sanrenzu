import datetime
import os
import uuid

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from ZPtest import settings
from email_demo import mail
from myapp.models import *


def company_home(request):
    return render(request, 'company_login.html')


def company_register_home(request):
    return render(request, 'company_regrster.html')


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
    yyzz = request.FILES.get('image_name')  # 将营业执照读出
    company = Companies()  # 实例化表对象
    company.login_name = login_name
    company.login_pwd = login_pwd
    company.company_name = company_name
    company.company_email = company_email
    company.company_phone = company_phone
    company.yyzz_img = yyzz  # 将营业执照读出来的图片对象与企业对象关联
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


def go_company_reset(request):
    if request.session.get('company_id'):
        return render(request, 'company_reset.html')
    else:
        return render(request, 'company_login.html')


def go_company_mine(request):  # 公司主页
    id = request.session.get('company_id')
    if id:
        company = Companies.objects.get(pk=id)
        company_zhiwei = company.job_set.all()
        leng = len(company_zhiwei)
        num_t = 0
        num_w = 0
        s_list = []
        for i in company_zhiwei:
            n = len(i.resume.all())
            for j in Record.objects.filter(job=company.id):
                if j.resume_state == '否':
                    num_w += 1
                    s_list.append(Resume.objects.get(pk=j.resume))
            num_t += n
        job_sy = company.release_surplus
        load_sy = company.downlode_surplus
        mail_sy = company.email_surplus
        s_lists = s_list[:4]
        if company_zhiwei:
            info = company_zhiwei.first().job_name
            xs_lists = Resume.objects.filter(job_title=info)[:3]
        return render(request, 'company_mine.html', locals())
    else:
        return redirect(reverse('NB:company_home'))


def go_company_zhiweisousuo(request, pagenum=1):
    id = request.session.get('company_id')
    if id:
        jobs = Job.objects.filter(company_id=id, state='保存并发布')
        paginator = Paginator(jobs, 3)
        try:
            page = paginator.page(pagenum)
        except:
            page = paginator.page(1)
        return render(request, 'company_zhiweilist.html', locals())
    else:
        return render(request, 'company_login.html')


def go_cpmpany_shoujianxiang(request, pagenum=1):
    id = request.session.get('company_id')
    if id:
        list = []
        jobs = Job.objects.filter(company_id=id, state='保存并发布')
        for job in jobs:
            for resume in job.resume.all():
                list.append(resume)
        paginator = Paginator(list, 15)
        try:
            page = paginator.page(pagenum)
        except:
            page = paginator.page(1)
        return render(request, 'company_shoujianxiang.html', locals())
    else:
        return render(request, 'company_login.html')


def go_company_vip(request):
    if request.session.get('company_id'):
        return render(request, 'company_vip.html')
    else:
        return render(request, 'company_login.html')


def go_company_recaija(request, pagenum=1):  # 公司人才夹
    id = request.session.get('company_id')
    if id:
        list = []
        r_jias = Checks.objects.filter(company=id, talent=1)
        for jia in r_jias:
            list.append(Resume.objects.get(pk=jia.resume.id))
        paginator = Paginator(list, 16)
        try:
            page = paginator.page(pagenum)
        except:
            page = paginator.page(1)
        return render(request, 'company_rencaijia.html', locals())
    else:
        return render(request, 'company_login.html')


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


def change_company(request):
    id = request.session.get('company_id')
    if id:
        com = Companies.objects.get(pk=id)
        l_name = com.login_name
        email = com.company_email
        phone = com.company_phone
        name = com.company_name
        info = com.company_info
        return render(request, 'company_change.html', locals())
    else:
        return redirect(reverse('NB:company_home'))


def change_company_info(request):
    name = request.POST.get('company_name')
    info = request.POST.get('com_info')
    com = Companies.objects.filter(login_name=name).first()
    com.company_info = info
    com.save()
    return render(request, 'company_mine.html', locals())


def check_resume(request, id):  # 企业浏览简历
    c_id = request.session.get('company_id')
    if c_id:
        resume = Resume.objects.filter(user_id=id)
        check = Checks.objects.filter(company_id=c_id, resume_id=id).first()
        if resume.exists():
            new_check = Checks()
            new_check.resume_id = id
            new_check.company_id = c_id
            new_check.save()
            # 插入数据到查看记录表
            resume = resume.first()
            name = resume.user_name
            img = resume.resume_img
            sex = resume.sex
            age = resume.age
            year = resume.work_year
            phone = resume.phone
            status = resume.state
            email = resume.email
            city = resume.city
            money = resume.month_money
            job_title = resume.job_title
            job_suffer = resume.job_suffer
            edu = resume.edu
            user_info = resume.user_info
            skill = resume.skill
            project_suffer = resume.project_suffer
            resume_state = resume.resume_state
            xueli = resume.xueli
            if check.download == 1:
                return render(request, 'resume_xiazai.html', locals())
        return render(request, 'resume_show.html', locals())
    else:
        return redirect(reverse('NB:company_home'))


def download_resume(request):
    c_id = request.session.get('company_id')
    if c_id:
        com = Companies.objects.get(pk=c_id)
        data = {}
        if com.downlode_surplus >= 1:
            id = request.GET.get("s_id")
            check = Checks.objects.filter(resume_id=id, company_id=c_id).first()
            check.download = 1
            check.save()
            com.downlode_surplus -= 1
            resume = Resume.objects.get(pk=id)
            data['name'] = resume.user_name
            data['phone'] = resume.phone
            data['email'] = resume.email
            data['status'] = "200"
        else:
            data['status'] = "404"
        return JsonResponse(data)
    else:
        return redirect(reverse('NB:company_home'))


def jiaru_resume(request):
    c_id = request.session.get('company_id')
    if c_id:
        data = {}
        id = request.GET.get("se_id")
        check = Checks.objects.filter(resume_id=id, company_id=c_id).first()
        check.talent = 1
        check.save()
        data['status'] = "200"
        return JsonResponse(data)
    else:
        return redirect(reverse('NB:company_home'))


def goumai_vip(request):
    c_id = request.session.get('company_id')
    if c_id:
        com = Companies.objects.get(pk=c_id)
        num = request.GET.get("num")
        data = {}
        print('-----------', num)
        if num == '1':
            com.email_surplus = 500
            com.release_surplus = 20
            com.downlode_surplus = 1500
            com.save()
            data['status'] = "200"
        elif num == '2':
            com.email_surplus = 500
            com.release_surplus = 20
            com.downlode_surplus = 1500
            com.save()
            data['status'] = "200"
        elif num == '3':
            com.email_surplus = 500
            com.release_surplus = 20
            com.downlode_surplus = 1500
            com.save()
            data['status'] = "200"
        else:
            data['status']
        return JsonResponse(data)
    else:
        return redirect(reverse('NB:company_home'))


def job_release(request):
    c_id = request.session.get('company_id')
    if c_id:
        job_name = request.POST.get('job_name')
        money = request.POST.get('money')
        academic = request.POST.get('academic')
        work_year = request.POST.get('work_year')
        gwzz = request.POST.get('gwzz')
        job_city = request.POST.get('job_city')
        state = request.POST.get('state')
        job = Job()
        job.job_name = job_name
        job.money = money
        job.xueli = academic
        job.work_year = work_year
        job.gwzz = gwzz
        job.state = state
        job.job_city = job_city
        job.company_id = c_id
        job.jon_time = str(datetime.datetime.now()).split('.')[0]
        job.text = job_name + money + academic + work_year + gwzz + job_city + state
        job.save()
        print(job_name, money, academic, work_year, gwzz, state, job_city)
        return render(request, 'company_mine.html')
    else:
        return redirect(reverse('NB:company_home'))


def xia_xian(request, id):
    c_id = request.session.get('company_id')
    if c_id:
        job = Job.objects.get(pk=id)
        job.state = "保存"
        job.save()
    return redirect(reverse('NB:go_company_zhiweisousuo', args=(1,)))


def re_resume(request, id):
    c_id = request.session.get('company_id')
    if c_id:
        resume = Resume.objects.filter(user_id=id)
        if resume.exists():
            new_check = Checks()
            new_check.resume_id = id
            new_check.company_id = c_id
            new_check.save()
            # 插入数据到查看记录表
            resume = resume.first()
            name = resume.user_name
            img = resume.resume_img
            sex = resume.sex
            age = resume.age
            year = resume.work_year
            phone = resume.phone
            status = resume.state
            email = resume.email
            city = resume.city
            money = resume.month_money
            job_title = resume.job_title
            job_suffer = resume.job_suffer
            edu = resume.edu
            user_info = resume.user_info
            skill = resume.skill
            project_suffer = resume.project_suffer
            resume_state = resume.resume_state
            xueli = resume.xueli
        return render(request, 'shoujian_show.html', locals())
    else:
        return redirect(reverse('NB:company_home'))


def company_name(request):
    data = {}
    name = request.GET.get('name')
    if Companies.objects.filter(company_name=name):
        data['status'] = 200
        return JsonResponse(data)
    else:
        data['status'] = 404
        return JsonResponse(data)


def company_user_name(request):  # 查看数据库中用户名是否存在
    data = {}
    shenfen = request.GET.get('shenfen')
    name = request.GET.get('name')
    print(shenfen, name)
    if shenfen == 'company':
        if Companies.objects.filter(login_name=name):
            data['status'] = 200
            return JsonResponse(data)
        else:
            data['status'] = 404
            return JsonResponse(data)
    if shenfen == 'user':
        if Users.objects.filter(login_name=name):
            data['status'] = 200
            return JsonResponse(data)
        else:
            data['status'] = 404
            return JsonResponse(data)


def search_company_job(request, pagenum=1):
    job_name = request.GET.get('job_name')
    xueli = request.GET.get('xueli')
    jingyan = request.GET.get('jingyan')
    xinzi = request.GET.get('xinzi')
    gangwei = request.GET.get('gangwei')
    qiwang = request.GET.get('qiwang')
    print(job_name, xueli, jingyan, xinzi, gangwei, qiwang)
    job = Resume.objects.all()
    if job_name == '':
        job1 = job
    else:
        job1 = job.extra(where=['text like "%%' + job_name + '%%"'])
    if xueli == '选择学历' or xueli == '不限':
        job2 = job1
    else:
        job2 = job1.extra(where=['xueli="' + xueli + '"'])
    if jingyan == '工作年限' or jingyan == '不限':
        job3 = job2
    else:
        job3 = job2.extra(where=['work_year="' + jingyan + '"'])
    if xinzi == '薪资要求' or xinzi == '不限':
        job4 = job3
    else:
        job4 = job3.extra(where=['month_money="' + xinzi + '"'])
    if gangwei == '岗位' or gangwei == '不限':
        job5 = job4
    else:
        job5 = job4.extra(where=['job_title="' + gangwei + '"'])
    if qiwang == '期望工作地点' or qiwang == '不限':
        job6 = job5
    else:
        job6 = job5.extra(where=['city="' + qiwang + '"'])
    paginator = Paginator(job6, 16)
    try:
        page = paginator.page(pagenum)
    except:
        page = paginator.page(1)
    return render(request, 'resume_sousuo.html', locals())


def user_home(request):
    return render(request, 'user/user_login.html')


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
            user = users_phone_login.first()
            request.session['user_id'] = user.id
        if users_email_login:
            user = users_email_login.first()
            request.session['user_id'] = user.id
        return redirect(reverse('NB:go_user_mine'))
    else:
        return redirect(reverse('NB:user_home'))


def user_register_home(request):
    return render(request, 'user/user_regrster.html')


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


def go_user_mine(request):
    if request.session.get('user_id'):
        return render(request, 'user/user_mine.html')
    else:
        return redirect(reverse('NB:user_home'))


def go_user_reset(request):
    return render(request, 'user/user_reset.html')


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


def go_user_vip(request):
    if request.session.get('user_id'):
        return render(request, 'user/user_vip.html')
    else:
        return render(request, 'user/user_login.html')


def company_show(request, id):  # 公司信息显示
    if request.session.get('user_id'):
        company_ = Companies.objects.filter(pk=id)
        if company_.exists():
            company_ = company_.first()
            com_name = company_.company_name
            com_info = company_.company_info
            return render(request, 'user/company_show.html', locals())
    else:
        return render(request, 'user/user_login.html')


def zhiwei_show(request, id):  # 职位信息显示
    if request.session.get('user_id'):
        job_ = Job.objects.filter(pk=id)
        if job_.exists():
            job_ = job_.first()
            name = job_.job_name
            money = job_.money
            xueli = job_.xueli
            addr = job_.job_city
            year = job_.work_year
            gwzz = job_.gwzz
            com_name = job_.company.company_name
            com_info = job_.company.company_info
            return render(request, 'user/job_show.html', locals())
    else:
        return render(request, 'user/user_login.html')


def go_user_zwsc(request, pagenum):  # 用户职位收藏页面
    if request.session.get('user_id'):
        user_id = request.session.get('user_id')
        shoucang = Collect.objects.filter(user_id=user_id)
        if shoucang.exists():
            job = Job.objects.filter(pk__in=[i.job_id for i in shoucang])
            paginator = Paginator(job, 3)
        else:
            paginator = Paginator(shoucang, 3)
        try:
            page = paginator.page(pagenum)
        except:
            page = paginator.page(1)
        return render(request, 'user/user_zhiweishoucang.html', locals())
    else:
        return render(request, 'user/user_login.html')


def zhiweishoucang_toudi(request):  # 用户职位投递
    id = request.GET['s_id']
    if request.session.get('user_id'):
        user_id = request.session.get('user_id')
        resume = Resume.objects.filter(user_id=user_id)
        if resume.exists():
            resume = resume.first()
            resume_id = resume.id
            recode_ = Record.objects.filter(job_id=id, resume_id=resume_id)
            if recode_.exists():
                data = {
                    'status': '901'
                }
            else:
                new_recode = Record()
                new_recode.resume_state = '已投递'
                new_recode.job_id = id
                new_recode.resume_id = resume_id
                new_recode.save()
                data = {
                    'status': '200'
                }
        else:
            data = {
                'status': '900'
            }
        return JsonResponse(data)
    else:
        return render(request, 'user/user_login.html')


def zhiweishoucang_shanchu(request, id):  # 用户职位收藏删除
    if request.session.get('user_id'):
        user_id = request.session.get('user_id')
        new_collect = Collect.objects.filter(user_id=user_id, job_id=id)
        new_collect.delete()
        return redirect(reverse('NB:user_zwsc', args=(1,)))
    else:
        return render(request, 'user/user_login.html')


def go_user_tdjd(request, pagenum):  # 用户投递进度页面
    if request.session.get('user_id'):
        user_id = request.session.get('user_id')
        resume = Resume.objects.filter(user_id=user_id)
        if resume.exists():
            resume = resume.first()
            toudi = Record.objects.filter(resume_id=resume.id)
            paginator = Paginator(toudi, 3)
        else:
            paginator = Paginator(resume, 3)
        try:
            page = paginator.page(pagenum)
        except:
            page = paginator.page(1)
        return render(request, 'user/user_toudijindu.html', locals())
    else:
        return render(request, 'user/user_login.html')


def go_user_pbgs(request, pagenum):  # 用户屏蔽公司页面
    if request.session.get('user_id'):
        user_id = request.session.get('user_id')
        pingbi_company = Shield.objects.filter(user_id=user_id)
        if pingbi_company.exists():
            company_ = Companies.objects.filter(pk__in=[i.company_id for i in pingbi_company])
            paginator = Paginator(company_, 3)
        else:
            paginator = Paginator(pingbi_company, 3)
        try:
            page = paginator.page(pagenum)
        except:
            page = paginator.page(1)
        return render(request, 'user/user_pingbigongsi.html', locals())
    else:
        return render(request, 'user/user_login.html')


def pingbi_company(request):  # 屏蔽公司
    if request.session.get('user_id'):
        user_id = request.session.get('user_id')
        job_id = request.GET['se_id']
        job_ = Job.objects.filter(pk=job_id)
        if job_.exists():
            job_ = job_.first()
            company_id = job_.company.id
            shield_ = Shield.objects.filter(company_id=company_id, user_id=user_id)
            if shield_.exists():
                data = {
                    'status': '900'
                }
            else:
                new_shield = Shield()
                new_shield.user_id = user_id
                new_shield.company_id = company_id
                new_shield.save()
                data = {
                    'status': '200'
                }
            return JsonResponse(data)
    else:
        return render(request, 'user/user_login.html')


def cancel_pingbi(request, name):  # 用户取消屏蔽公司
    if request.session.get('user_id'):
        user_id = request.session.get('user_id')
        company = Companies.objects.filter(company_name=name)
        if company.exists():
            company = company.first()
            pingbi_company = Shield.objects.filter(company_id=company.id, user_id=user_id)
            if pingbi_company.exists():
                pingbi_company.delete()
                return redirect(reverse('NB:user_pbgs', args=(1,)))
    else:
        return render(request, 'user/user_login.html')


def go_user_skgw(request, pagenum):  # 用户谁看过我页面
    if request.session.get('user_id'):
        user_id = request.session.get('user_id')
        resume = Resume.objects.filter(user_id=user_id)
        if resume.exists():
            resume = resume.first()
            checks = Checks.objects.filter(resume_id=resume.id)
            print(checks)
            if checks.exists():
                company_ = Companies.objects.filter(pk__in=[i.company_id for i in checks])
                paginator = Paginator(company_, 3)
            else:
                paginator = Paginator(checks, 3)
        else:
            paginator = Paginator(resume, 3)
        try:
            page = paginator.page(pagenum)
        except:
            page = paginator.page(1)
        return render(request, 'user/user_skgw.html', locals())
    else:
        return render(request, 'user/user_login.html')


def go_user_jlll(request):  # 用户简历浏览页面
    if request.session.get('user_id'):
        user_id = request.session['user_id']
        resume = Resume.objects.filter(user_id=user_id)
        if resume.exists():
            resume = resume.first()
            name = resume.user_name
            img = resume.resume_img
            sex = resume.sex
            age = resume.age
            year = resume.work_year
            phone = resume.phone
            status = resume.state
            email = resume.email
            city = resume.city
            money = resume.month_money
            job_title = resume.job_title
            job_suffer = resume.job_suffer
            edu = resume.edu
            user_info = resume.user_info
            skill = resume.skill
            project_suffer = resume.project_suffer
            resume_state = resume.resume_state
            xueli = resume.xueli
        return render(request, 'user/user_resume_show.html', locals())
    else:
        return render(request, 'user/user_login.html')


def zwss_home(request, pagenum):  # 职位搜索
    if request.session.get('user_id'):
        job_ = Job.objects.filter(state='保存并发布')
        guanjianzi = request.POST.get('guanjianzi')
        xueli = request.POST.get('xueli')
        time = request.POST.get('time')
        money = request.POST.get('money')
        job = request.POST.get('job')
        city = request.POST.get('city')
        if guanjianzi == '':
            job1 = job_
        else:
            job1 = job_.extra(where=['text like "%%' + guanjianzi + '%%"'])
        if xueli == '学历':
            job2 = job1
        else:
            job2 = job1.extra(where=['xueli="' + xueli + '"'])
        if time == '工作时间' or time == '无':
            job3 = job2
        else:
            job3 = job2.extra(where=['work_year="' + time + '"'])
        if money == '薪资要求':
            job4 = job3
        else:
            job4 = job3.extra(where=['money="' + money + '"'])
        if job == '岗位':
            job5 = job4
        else:
            job5 = job4.extra(where=['job_name="' + job + '"'])
        if city == '期望工作地点':
            job6 = job5
        else:
            job6 = job5.extra(where=['job_city="' + city + '"'])
        paginator = Paginator(job6, 3)
        try:
            page = paginator.page(pagenum)
        except:
            page = paginator.page(1)
        return render(request, 'user/user_zhiweisousuo.html', locals())
    else:
        return render(request, 'user/user_login.html')


def find_resume(request):  # 判断简历是否存在
    if request.session.get('user_id'):
        user_id = request.session['user_id']
        resume = Resume.objects.filter(user_id=user_id)
        if resume.exists():
            return redirect(reverse("NB:resume_show"))
        else:
            return redirect(reverse("NB:resume_upload"))


def go_resume_upload(request):  # 简历上传
    if request.session.get('user_id'):
        return render(request, 'user/user_jlsc.html')
    else:
        return render(request, 'user/user_login.html')


def save_xinxi(request):  # 简历上传信息
    if request.session.get('user_id'):
        print(request.POST)
        name = request.POST.get('username')
        sex = request.POST.get('sex')
        age = request.POST.get('age')
        status = request.POST.get('job_status')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        suffer = request.POST.get('job_suffer')
        city = request.POST.get('city')
        money = request.POST.get('month_money')
        direction = request.POST.get('job_direction')
        edu = request.POST.get('edu')
        resume = request.POST.get('resume')
        skill = request.POST.get('skill')
        object = request.POST.get('object')
        job = request.POST.get('job')
        resume_status = request.POST.get('resume_status')
        xueli = request.POST.get('xueli')
        resume_img = request.FILES.get('resume_img')
        id = str(request.session['user_id'])
        resume_img.name = id + '_' + uuid.uuid4().hex + ('.jpg' if resume_img.content_type.endswith('jpeg') else '.png')
        new_resume = Resume()
        new_resume.user_name = name
        new_resume.sex = sex
        new_resume.age = age
        new_resume.work_year = suffer
        new_resume.phone = phone
        new_resume.state = status
        new_resume.email = email
        new_resume.city = city
        new_resume.month_money = money
        new_resume.job_title = direction
        new_resume.job_suffer = job
        new_resume.edu = edu
        new_resume.user_info = resume
        new_resume.skill = skill
        new_resume.project_suffer = object
        new_resume.resume_state = resume_status
        new_resume.xueli = xueli
        new_resume.resume_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        new_resume.resume_img = resume_img
        new_resume.text = direction + job + resume + skill + object
        new_resume.user_id = request.session['user_id']
        new_resume.save()
        return render(request, 'user/user_mine.html')
    else:
        return render(request, 'user/user_login.html')


def change_xinxi(request):  # 修改简历信息
    if request.session.get('user_id'):
        name = request.POST.get('username')
        sex = request.POST.get('sex')
        age = request.POST.get('age')
        status = request.POST.get('job_status')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        suffer = request.POST.get('job_suffer')
        city = request.POST.get('city')
        money = request.POST.get('month_money')
        direction = request.POST.get('job_direction')
        edu = request.POST.get('edu')
        resume = request.POST.get('resume')
        skill = request.POST.get('skill')
        object = request.POST.get('object')
        job = request.POST.get('job')
        resume_status = request.POST.get('resume_status')
        xueli = request.POST.get('xueli')
        resume_img = request.FILES.get('resume_img')
        if resume_img:
            user_id = str(request.session['user_id'])
            resume_img.name = user_id + '_' + uuid.uuid4().hex + (
                '.jpg' if resume_img.content_type.endswith('jpeg') else '.png')
            user_id = request.session['user_id']
            new_resume = Resume.objects.filter(user_id=user_id)
            if new_resume.exists():
                new_resume = new_resume.first()
                new_resume.resume_img = resume_img
        else:
            user_id = request.session['user_id']
            new_resume = Resume.objects.filter(user_id=user_id)
            if new_resume.exists():
                new_resume = new_resume.first()
        new_resume.user_name = name
        new_resume.sex = sex
        new_resume.age = age
        new_resume.work_year = suffer
        new_resume.phone = phone
        new_resume.state = status
        new_resume.email = email
        new_resume.city = city
        new_resume.month_money = money
        new_resume.job_title = direction
        new_resume.job_suffer = job
        new_resume.edu = edu
        new_resume.user_info = resume
        new_resume.skill = skill
        new_resume.project_suffer = object
        new_resume.resume_state = resume_status
        new_resume.xueli = xueli
        new_resume.resume_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        new_resume.text = direction + job + resume + skill + object
        new_resume.user_id = request.session['user_id']
        new_resume.save()
        return render(request, 'user/user_mine.html')
    else:
        return render(request, 'user/user_login.html')


def img(request):  # 简历照片异步加载
    if request.session.get('user_id'):
        id = str(request.session['user_id'])
        photoFile = request.FILES.get('photo')
        dir_ = os.path.join(settings.BASE_DIR, 'static/user/resume_img')
        file_name = id + '_' + uuid.uuid4().hex + ('.jpg' if photoFile.content_type.endswith('jpeg') else '.png')
        with open(os.path.join(dir_, file_name), 'wb') as f:
            for chunk in photoFile.chunks():
                f.write(chunk)
        return JsonResponse({'msg': 1, 'path': f'user/resume_img/{file_name}'})


def resume_refresh(request):  # 简历刷新
    if request.session.get('user_id'):
        user_id = request.session['user_id']
        new_resume = Resume.objects.filter(user_id=user_id)
        if new_resume.exists():
            new_resume = new_resume.first()
            new_resume.resume_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            new_resume.save()
            data = {
                'status': '200'
            }
        else:
            data = {
                'status': '900'
            }
        return JsonResponse(data)


def collect_zhiwei(request):  # 用户收藏职位
    id = request.GET['s_id']
    if request.session.get('user_id'):
        user_id = request.session.get('user_id')
        collect_ = Collect.objects.filter(job_id=id, user_id=user_id)
        if collect_.exists():
            data = {
                'status': '900'
            }
        else:
            new_collect = Collect()
            new_collect.user_id = user_id
            new_collect.job_id = id
            new_collect.save()
            data = {
                'status': '200'
            }
        return JsonResponse(data)
    else:
        return render(request, 'user/user_login.html')


def quit_login(request):
    request.session.flush()
    return render(request, 'company_login.html')
