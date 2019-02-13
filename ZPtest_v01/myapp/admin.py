from django.contrib import admin
from myapp.models import *

# Register your models here.

admin.site.register([Users, Companies, Resume, Collect, Job, Record, Shield, Vip, Checks])