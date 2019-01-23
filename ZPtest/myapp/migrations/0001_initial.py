# Generated by Django 2.0.6 on 2019-01-21 09:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Checks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'checks',
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('letter', models.CharField(max_length=5)),
            ],
            options={
                'db_table': 'city',
            },
        ),
        migrations.CreateModel(
            name='Collect',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'collect',
            },
        ),
        migrations.CreateModel(
            name='Companies',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login_name', models.CharField(max_length=12)),
                ('login_pwd', models.CharField(max_length=15)),
                ('company_name', models.CharField(max_length=50)),
                ('company_email', models.CharField(max_length=30)),
                ('company_phone', models.CharField(max_length=11)),
                ('vip_level', models.CharField(default='无', max_length=2)),
                ('company_info', models.TextField()),
                ('release_surplus', models.IntegerField(default=0)),
                ('downlode_surplus', models.IntegerField(default=0)),
                ('email_surplus', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'companys',
            },
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_name', models.CharField(max_length=10)),
                ('money', models.CharField(max_length=10)),
                ('gwzz', models.TextField()),
                ('rzzz', models.TextField()),
                ('job_city', models.CharField(max_length=15)),
                ('work_year', models.CharField(max_length=15)),
                ('xueli', models.CharField(max_length=10)),
                ('state', models.CharField(max_length=10)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.City')),
                ('collect', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Collect')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Companies')),
            ],
            options={
                'db_table': 'job',
            },
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resume_state', models.CharField(max_length=20)),
                ('job', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='myapp.Job')),
            ],
            options={
                'db_table': 'record',
            },
        ),
        migrations.CreateModel(
            name='Resume',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=20)),
                ('sex', models.CharField(max_length=10)),
                ('age', models.CharField(max_length=10)),
                ('work_year', models.CharField(max_length=10)),
                ('phone', models.IntegerField()),
                ('state', models.CharField(max_length=10)),
                ('email', models.CharField(max_length=30)),
                ('city', models.CharField(max_length=30)),
                ('month_money', models.CharField(max_length=10)),
                ('job_title', models.CharField(max_length=50)),
                ('job_suffer', models.CharField(max_length=100)),
                ('edu', models.CharField(max_length=50)),
                ('user_info', models.CharField(max_length=100)),
                ('skill', models.CharField(max_length=100)),
                ('text', models.TextField()),
                ('project_suffer', models.CharField(max_length=100)),
                ('resume_state', models.CharField(max_length=20)),
                ('xueli', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'resume',
            },
        ),
        migrations.CreateModel(
            name='Shield',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Companies')),
            ],
            options={
                'db_table': 'shield',
            },
        ),
        migrations.CreateModel(
            name='Talents',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('classify', models.CharField(max_length=10, null=True)),
                ('company', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='myapp.Companies')),
            ],
            options={
                'db_table': 'talents',
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login_name', models.CharField(max_length=12)),
                ('login_pwd', models.CharField(max_length=12)),
                ('vip', models.BooleanField(default=0)),
                ('user_phone', models.CharField(max_length=11)),
                ('user_email', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'users',
            },
        ),
        migrations.CreateModel(
            name='Vip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.CharField(max_length=10)),
                ('jon_num', models.IntegerField()),
                ('resume_num', models.IntegerField()),
                ('email_num', models.IntegerField()),
            ],
            options={
                'db_table': 'vip',
            },
        ),
        migrations.AddField(
            model_name='shield',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Users'),
        ),
        migrations.AddField(
            model_name='resume',
            name='talents',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Talents'),
        ),
        migrations.AddField(
            model_name='resume',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Users'),
        ),
        migrations.AddField(
            model_name='record',
            name='resume',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Resume'),
        ),
        migrations.AddField(
            model_name='collect',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='myapp.Users'),
        ),
        migrations.AddField(
            model_name='checks',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Companies'),
        ),
        migrations.AddField(
            model_name='checks',
            name='resume',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Resume'),
        ),
    ]
