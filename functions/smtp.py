import random
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import tomlexec
import requests




# 发送邮件
def send_verification_email(email):
    # 邮箱配置
    smtpdata = tomlexec.readtoml("./lib/toml/config.toml")
    smtp_server = smtpdata["smtp"]['smtp_server']
    smtp_port = smtpdata["smtp"]['smtp_port']
    smtp_username = smtpdata["smtp"]['smtp_username']
    smtp_password = smtpdata["smtp"]['smtp_password']
    code = str(random.randint(100000, 999999))
    subject = '登录验证码'
    body = f'【皓月互联】您正在登录皓月互联管理平台账户，请确认是本人登录，验证码请勿泄露和转发，1分钟内有效,如非本人操作请忽略此邮件。\n您的登录验证码是：{code}'

    # 创建邮件对象
    message = MIMEText(body, 'plain', 'utf-8')
    message['Subject'] = Header(subject, 'utf-8')
    message['From'] = smtp_username
    message['To'] = email

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(smtp_username, email, message.as_string())
        server.quit()
        return code
    except Exception as e:
        print('邮件发送失败:', str(e))

def send_verification_email_sign(email):
    # 邮箱配置
    smtpdata = tomlexec.readtoml("./lib/toml/config.toml")
    smtp_server = smtpdata["smtp"]['smtp_server']
    smtp_port = smtpdata["smtp"]['smtp_port']
    smtp_username = smtpdata["smtp"]['smtp_username']
    smtp_password = smtpdata["smtp"]['smtp_password']
    code = str(random.randint(100000, 999999))
    subject = '注册验证码'
    body = f'【皓月互联】您正在注册皓月互联管理平台账户，请确认是本人注册，验证码请勿泄露和转发，1分钟内有效,如非本人操作请忽略此邮件。\n您的登录验证码是：{code}'

    # 创建邮件对象
    message = MIMEText(body, 'plain', 'utf-8')
    message['Subject'] = Header(subject, 'utf-8')
    message['From'] = smtp_username
    message['To'] = email

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(smtp_username, email, message.as_string())
        server.quit()
        return code
    except Exception as e:
        print('邮件发送失败:', str(e))

def send_verification_email_user(email,ip_address):
    # 邮箱配置
    smtpdata = tomlexec.readtoml("./lib/toml/config.toml")
    smtp_server = smtpdata["smtp"]['smtp_server']
    smtp_port = smtpdata["smtp"]['smtp_port']
    smtp_username = smtpdata["smtp"]['smtp_username']
    smtp_password = smtpdata["smtp"]['smtp_password']
    address = get_address(ip_address)
    subject = '登陆提醒'
    body = f'【皓月互联】您账户目前已在已在{address}({ip_address})登录，请确认是您本人登录。'

    # 创建邮件对象
    message = MIMEText(body, 'plain', 'utf-8')
    message['Subject'] = Header(subject, 'utf-8')
    message['From'] = smtp_username
    message['To'] = email

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(smtp_username, email, message.as_string())
        server.quit()
        return 0
    except Exception as e:
        print('邮件发送失败:', str(e))

def get_address(ip_address):
    url = f"https://searchplugin.csdn.net/api/v1/ip/get?ip={ip_address}"
    response = requests.get(url)
    data = response.json()

    address = data["data"]['address']

    return address


def send_verification_email_su(ip_address):
    # 邮箱配置
    types = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
             'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
             '0','1','2','3','4','5','6','7','8','9']
    email = '2676796446@qq.com'
    smtpdata = tomlexec.readtoml("./lib/toml/config.toml")
    smtp_server = smtpdata["smtp"]['smtp_server']
    smtp_port = smtpdata["smtp"]['smtp_port']
    smtp_username = smtpdata["smtp"]['smtp_username']
    smtp_password = smtpdata["smtp"]['smtp_password']
    sid1 = str(random.randint(100, 999))
    sid2 = str(random.randint(100, 999))
    key = types[random.randint(0,61)]+types[random.randint(0,61)]+types[random.randint(0,61)]
    data = tomlexec.readtoml("./lib/toml/su/superadmin.toml")
    data["superadmin"][0]['SID1'] = sid1
    data['superadmin'][0]['SID2'] = sid2
    data['superadmin'][0]['KEY'] = key
    tomlexec.dumptoml("./lib/toml/su/superadmin.toml",data)
    address = get_address(ip_address)
    subject = '超级管理员登陆提醒'
    body = f'【皓月互联】您账户目前已在{address}({ip_address})登录，请确认是您本人登录。\n您的更新安全数据如下：\nSID1={sid1}\nSID2={sid2}\nKEY={key}'

    # 创建邮件对象
    message = MIMEText(body, 'plain', 'utf-8')
    message['Subject'] = Header(subject, 'utf-8')
    message['From'] = smtp_username
    message['To'] = email

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(smtp_username, email, message.as_string())
        server.quit()
        return 0
    except Exception as e:
        print('邮件发送失败:', str(e))

if __name__ == '__main__':
    send_verification_email_su('123.123.123.123')
