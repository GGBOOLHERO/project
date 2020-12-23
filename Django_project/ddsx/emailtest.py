# 编写客户端发送邮件
# 1. 导入模块
import smtplib  # 服务器模块
from email.mime.text import MIMEText  # 构建邮件模块

# 2. 构建邮件
text = MIMEText('这是文章主体\n')
# 头部
text['subject'] = '主题'
# 发件人邮件
text['from'] = 'ggbool@163.com'
# 收件人
text['to'] = '1798270890@qq.com'


# 3. 登录 163 服务器
smtp = smtplib.SMTP_SSL(host='smtp.163.com', port=994)
print(smtp)
# smtp.ehlo()
# smtp.starttls()
smtp.set_debuglevel(1)
smtp.login('ggbool@163.com', 'XWQNHBVXAKHFHBRF')

# 4. 发送邮件
smtp.sendmail('ggbool@163.com', ['1798270890@qq.com'], text.as_string())
smtp.close()