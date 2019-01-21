"""
邮件发送系统
my_sender ：发件人的账号
your_user ：收件人的账号
my_password ：登录邮箱的授权码
仅供内部使用,禁止外传
作者：凡凡  代码简单切勿嘲笑
"""
import smtplib
from email.mime.text import MIMEText
from email.header import Header


def mail(my_sender='liao_fanfan@163.com', my_password='Liaofan33', your_user='', content_text='密码找回', title_text=''):
    try:
        msg = MIMEText(content_text, 'plain', 'utf-8')
        msg['From'] = my_sender  # 发件人的邮箱昵称和邮箱账号
        msg['To'] = your_user  # 收件人的邮箱昵称和邮箱账号
        msg['Subject'] = Header(title_text, 'utf-8')  # 邮箱主题

        server = smtplib.SMTP('smtp.163.com', 25)  # 邮箱协议地址和端口
        server.login(my_sender, my_password)  # 登录：邮箱账号密码
        server.sendmail(my_sender, [your_user, ], msg.as_string())
        print(your_user, '发送成功')
        server.close()  # 关闭
        server.quit()  # 退出
    except smtplib.SMTPException as e:
        print(e)


