from django.contrib import admin
from myapp.models import *

# Register your models here.

admin.site.register([Users, Companies, Talents, Resume, Collect, City, Job, Record, Shield, Vip, Checks])