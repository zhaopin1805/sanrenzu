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
    path('user_set/', email_phone_set, name='user_set'),
    path('user_reset/', email_phone_reset, name='user_reset'),
    path('company_set/', email_phone_set, name='company_set'),
    path('company_reset/', email_phone_reset, name='company_reset'),
    path('set_phone/', set_phone, name='set_phone'),
    path('set_email/', set_email, name='set_email')
]
