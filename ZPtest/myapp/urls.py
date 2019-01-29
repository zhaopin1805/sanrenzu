from django.urls import path

from myapp.views import *

app_name = 'NB'

urlpatterns = [
    path('user_home/', user_home, name='user_home'),
    path('company_home/', company_home, name='company_home'),
    path('user_register_home/', user_register_home, name='user_register_home'),
    path('company_register_home/', company_register_home, name='company_register_home'),
    path('user_register/', user_register, name='user_register'),
    path('company_register/', company_register, name='company_register'),
    path('user_login/', user_login, name='user_login'),
    path('company_login/', company_login, name='company_login'),
    path('go_user_reset/', go_user_reset, name='go_user_reset'),
    path('go_company_reset/', go_company_reset, name='go_company_reset'),
    path('go_company_mine/', go_company_mine, name='go_company_mine'),
    path('go_user_mine/', go_user_mine, name='go_user_mine'),
    path('go_user_vip/', go_user_vip, name='go_user_vip'),
    path('go_user_vip/', go_company_vip, name='go_company_vip'),
    path('go_company_zhiweisousuo/', go_company_zhiweisousuo, name='go_company_zhiweisousuo'),
    path('go_company_shoujianxiang/', go_cpmpany_shoujianxiang, name='go_cpmpany_shoujianxiang'),
    path('go_company_rencaijia/', go_company_recaija, name='go_company_recaija'),
    path('upload_job_home/', upload_job_home, name='upload_job_home'),
    path('save_job/', save_job, name='save_job'),
    path('save_xinxi/', save_xinxi, name='save_xinxi'),
    path('user_set/', email_phone_set, name='user_set'),
    path('user_reset/', email_phone_reset, name='user_reset'),
    path('upload_resume_home/', upload_resume_home, name='upload_resume_home'),
    path('zwss_home/', zwss_home, name='zwss_home'),
    path('company_set/', email_phone_set, name='company_set'),
    path('company_reset/', email_phone_reset, name='company_reset'),
    path('set_phone/', set_phone, name='set_phone'),
    path('set_email/', set_email, name='set_email')
]
