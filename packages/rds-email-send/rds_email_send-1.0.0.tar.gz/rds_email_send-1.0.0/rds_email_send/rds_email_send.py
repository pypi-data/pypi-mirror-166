import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

# 邮件发送的用户名和密码 常识:第三方授权码
_user='DMS@cellprobio.com'
_pwd='ArvRrGyD2eSPQLLP'

now =time.strftime('%Y-%m-%d %H:%M:%S') # 获取时间戳

class SendEmail:
    def send_email(self,email_to,files_path):
        """
        email_to 收件方
        filepath 发送的附件地址/路径

        """
        # 如名字所示 MUltipart就是多个部分
        msg=MIMEMultipart()
        #主题
        msg['Subject']=now+" 上传结果报告"
        msg['From']=_user
        msg['To']=email_to

        # --这是文字部分--
        html_msg ="""
        <p>修改路径</p>
        <p><a href="http://192.168.1.13/k3cloud">金蝶链接</a></p>
         """
        msg.attach(MIMEText(html_msg, 'html', 'utf-8'))

        # --这是附件部分--
        if isinstance(files_path,str):
            part = MIMEApplication(open(files_path,'rb').read())
            part.add_header('Content-Disposition','attachment',filename=files_path)
            msg.attach(part)
        else:
            # files_paths = ['路径1', '路径2']
            for file_path in files_path:
                part = MIMEApplication(open(file_path, 'rb').read())
                part.add_header('Content-Disposition', 'attachment', filename=file_path)
                msg.attach(part)

        s=smtplib.SMTP_SSL("smtp.exmail.qq.com",timeout=465) #链接smtp邮件服务器,端口默认25
        s.login(_user,_pwd) #登录服务器
        s.sendmail(_user,email_to,msg.as_string()) #发送邮件
        print("邮件发送成功")
        s.close()

if __name__ == '__main__':
    SendEmail().send_email('9********4@qq.com',['路径1','路径2'])