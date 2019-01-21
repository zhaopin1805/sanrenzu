"""
简历表：关联User，Talents，Record,Check表
其中User，Talents为多方表，Record，Check为一方表
"""

from django.db import models


class Users(models.Model):  # 用户表
    # user_id = models.IntegerField(primary_key=True, auto_created=False)
    login_name = models.CharField(max_length=12)
    login_pwd = models.CharField(max_length=12)
    vip = models.BooleanField(default=0)  # 0表示非会员，1表示会员
    user_phone = models.CharField(max_length=11)
    user_email = models.CharField(max_length=30)

    class Meta:
        db_table = 'users'


class Companies(models.Model):  # 企业表
    # company_id = models.IntegerField(primary_key=True, auto_created=False)
    login_name = models.CharField(max_length=12)
    login_pwd = models.CharField(max_length=15)
    company_name = models.CharField(max_length=50)
    company_email = models.CharField(max_length=30)
    company_phone = models.CharField(max_length=11)
    vip_level = models.CharField(max_length=2, default='无')
    company_info = models.TextField()
    release_surplus = models.IntegerField(default=0)
    downlode_surplus = models.IntegerField(default=0)
    email_surplus = models.IntegerField(default=0)

    class Meta:
        db_table = 'companys'


class Talents(models.Model):  # 人才表
    # talents_id = models.IntegerField(primary_key=True, auto_created=False)
    company = models.OneToOneField(Companies, on_delete=models.CASCADE)  # 一方主动方关联企业表
    classify = models.CharField(max_length=10, null=True)

    class Meta:
        db_table = 'talents'


class Resume(models.Model):  # 简历表
    # resume_id = models.IntegerField(primary_key=True, auto_created=False)
    # 关联User表，一对多关系，简历表为多方表
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    # 关联Talents表，一对多关系，简历表为多方表
    talents = models.ForeignKey(Talents, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=20)
    sex = models.CharField(max_length=10)
    age = models.CharField(max_length=10)
    work_year = models.CharField(max_length=10)
    phone = models.IntegerField()
    state = models.CharField(max_length=10)
    email = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    month_money = models.CharField(max_length=10)
    job_title = models.CharField(max_length=50)
    job_suffer = models.CharField(max_length=100)
    edu = models.CharField(max_length=50)
    user_info = models.CharField(max_length=100)
    skill = models.CharField(max_length=100)
    text = models.TextField()
    project_suffer = models.CharField(max_length=100)
    resume_state = models.CharField(max_length=20)
    xueli = models.CharField(max_length=20)

    class Meta:
        db_table = 'resume'


class Collect(models.Model):  # 职位收藏表
    # collect_id = models.IntegerField(auto_created=False, primary_key=True)
    user = models.OneToOneField(Users, on_delete=models.CASCADE)

    class Meta:
        db_table = 'collect'


# 城市表City
class City(models.Model):
    # city_id = models.IntegerField(primary_key=True, auto_created=False)
    name = models.CharField(max_length=20)
    letter = models.CharField(max_length=5)

    class Meta:
        db_table = 'city'


class Job(models.Model):  # 职位表
    # job_id = models.IntegerField(auto_created=True, primary_key=False)
    company = models.ForeignKey(Companies, on_delete=models.CASCADE)  # 关联公司表，多方
    job_name = models.CharField(max_length=10)
    money = models.CharField(max_length=10)
    gwzz = models.TextField()  # 岗位职责
    rzzz = models.TextField()
    job_city = models.CharField(max_length=15)
    work_year = models.CharField(max_length=15)
    xueli = models.CharField(max_length=10)
    state = models.CharField(max_length=10)
    collect = models.ForeignKey(Collect, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    class Meta:
        db_table = 'job'


class Record(models.Model):  # 投递记录表
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)  # 多方关联简历表
    # record_id = models.IntegerField(primary_key=True, auto_created=False)
    job = models.OneToOneField(Job, on_delete=models.CASCADE)  # 一方主动方关联职位表
    resume_state = models.CharField(max_length=20)

    class Meta:
        db_table = 'record'


class Shield(models.Model):  # 屏蔽公司表
    # shield_id = models.IntegerField(primary_key=True, auto_created=False)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)  # 多方关联用户表
    company = models.ForeignKey(Companies, on_delete=models.CASCADE)  # 多方关联企业表

    class Meta:
        db_table = 'shield'


class Vip(models.Model):  # 套餐表
    # vip_id = models.IntegerField(auto_created=False, primary_key=True)
    grade = models.CharField(max_length=10)
    jon_num = models.IntegerField()
    resume_num = models.IntegerField()
    email_num = models.IntegerField()

    class Meta:
        db_table = 'vip'


class Checks(models.Model):  # 查看纪录表
    # check_id = models.IntegerField(auto_created=False, primary_key=True)
    company = models.ForeignKey(Companies, on_delete=models.CASCADE)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)

    class Meta:
        db_table = 'checks'
