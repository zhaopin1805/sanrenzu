# Generated by Django 2.1.5 on 2019-01-19 02:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Check',
            fields=[
                ('check_id', models.IntegerField(auto_created=True, primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'check',
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('city_id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20, null=True)),
                ('letter', models.CharField(max_length=5, null=True)),
            ],
            options={
                'db_table': 'city',
            },
        ),
        migrations.CreateModel(
            name='Collect',
            fields=[
                ('collect_id', models.IntegerField(auto_created=True, primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'collect',
            },
        ),
        migrations.CreateModel(
            name='Companies',
            fields=[
                ('company_id', models.IntegerField(auto_created=True, primary_key=True, serialize=False)),
                ('login_name', models.CharField(max_length=12)),
                ('login_pwd', models.CharField(max_length=15)),
                ('company_name', models.CharField(max_length=50, null=True)),
                ('company_email', models.CharField(max_length=30, null=True)),
                ('company_phone', models.CharField(max_length=11)),
                ('vip_level', models.CharField(max_length=2)),
                ('company_info', models.TextField()),
                ('release_surplus', models.IntegerField()),
                ('downlode_surplus', models.IntegerField()),
                ('email_surplus', models.IntegerField()),
            ],
            options={
                'db_table': 'company',
            },
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('job_id', models.IntegerField(auto_created=True, primary_key=True, serialize=False)),
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
                ('record_id', models.IntegerField(primary_key=True, serialize=False)),
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
                ('resume_id', models.IntegerField(primary_key=True, serialize=False)),
                ('user_name', models.CharField(max_length=20, null=True)),
                ('sex', models.CharField(max_length=10, null=True)),
                ('age', models.CharField(max_length=10, null=True)),
                ('work_year', models.CharField(max_length=10, null=True)),
                ('phone', models.IntegerField(max_length=10, null=True)),
                ('state', models.CharField(max_length=10, null=True)),
                ('email', models.CharField(max_length=30, null=True)),
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
                ('shield_id', models.IntegerField(primary_key=True, serialize=False)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Companies')),
            ],
            options={
                'db_table': 'shield',
            },
        ),
        migrations.CreateModel(
            name='Talents',
            fields=[
                ('talents_id', models.IntegerField(primary_key=True, serialize=False)),
                ('classify', models.CharField(max_length=10, null=True)),
                ('company', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='myapp.Companies')),
            ],
            options={
                'db_table': 'talents',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.IntegerField(primary_key=True, serialize=False)),
                ('login_name', models.CharField(max_length=12)),
                ('login_pwd', models.CharField(max_length=12)),
                ('vip', models.BooleanField(default=0)),
                ('user_phone', models.CharField(max_length=11)),
                ('user_email', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'use',
            },
        ),
        migrations.CreateModel(
            name='Vip',
            fields=[
                ('vip_id', models.IntegerField(auto_created=True, primary_key=True, serialize=False)),
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
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.User'),
        ),
        migrations.AddField(
            model_name='resume',
            name='talents',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Talents'),
        ),
        migrations.AddField(
            model_name='resume',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.User'),
        ),
        migrations.AddField(
            model_name='record',
            name='resume',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Resume'),
        ),
        migrations.AddField(
            model_name='collect',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='myapp.User'),
        ),
        migrations.AddField(
            model_name='check',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Companies'),
        ),
        migrations.AddField(
            model_name='check',
            name='resume',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Resume'),
        ),
    ]
