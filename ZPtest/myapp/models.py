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
    yyzz_img = models.ImageField(upload_to='company/%Y-%m-%d')
    company_info = models.TextField()
    release_surplus = models.IntegerField(default=0)
    downlode_surplus = models.IntegerField(default=0)
    email_surplus = models.IntegerField(default=0)
    user = models.ManyToManyField(Users, through='Shield')

    class Meta:
        db_table = 'companys'


class Resume(models.Model):  # 简历表
    # resume_id = models.IntegerField(primary_key=True, auto_created=False)
    # 关联User表，一对多关系，简历表为多方表
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    # 关联Talents表，一对多关系，简历表为多方表
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
    resume_time = models.CharField(max_length=20)  # 刷新时间
    resume_img = models.ImageField(upload_to='user/%Y-%m-%d')
    company = models.ManyToManyField(Companies, through='Checks')

    class Meta:
        db_table = 'resume'


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
    job_city = models.CharField(max_length=15)
    work_year = models.CharField(max_length=15)
    xueli = models.CharField(max_length=10)
    state = models.CharField(max_length=10)
    jon_time = models.CharField(max_length=20)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    resume = models.ManyToManyField(Resume, through='Record')
    user = models.ManyToManyField(Users, through='Collect')

    class Meta:
        db_table = 'job'


# class Talents(models.Model):  # 人才表(第三方表)
#     company = models.ForeignKey(Companies, on_delete=models.CASCADE)  # 关联企业
#     resume = models.ForeignKey(Resume, on_delete=models.CASCADE)  # 关联简历
#     classify = models.CharField(max_length=10, null=True)
#
#     class Meta:
#         db_table = 'talents'


class Collect(models.Model):  # 职位收藏表（第三方表）职位表主动方
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)

    class Meta:
        db_table = 'collect'


class Record(models.Model):  # 投递记录表（第三方表）职位表主动方
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)  # 简历表外键
    job = models.ForeignKey(Job, on_delete=models.CASCADE)  # 职位表外键
    resume_state = models.CharField(max_length=20)

    class Meta:
        db_table = 'record'


class Shield(models.Model):  # 屏蔽公司表(第三方表)公司表主动方
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


# 由于人才夹表和查看纪录表都是企业和简历的多对多关系第三方表，所以舍弃人才夹表，在查看记录表里添加是否被收藏字段，

class Checks(models.Model):  # 查看纪录表(第三方表)简历表主动方
    company = models.ForeignKey(Companies, on_delete=models.CASCADE)  # 关联企业表
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)  # 关联简历表，
    Talent = models.CharField(default=0)  # 0表示未被收藏，1表示被收藏，人才夹直接在此表查找talent字段是1的简历就行
    classify = models.CharField(max_length=10, null=True)  # 人才夹的分类

    class Meta:
        db_table = 'checks'
