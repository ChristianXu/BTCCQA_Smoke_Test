__author__ = 'sara'

import smtplib
import time
from email.mime.text import MIMEText
from email.header import Header


class SendEmail:
    def __init__(self):

        self.mail_host = "smtp.gmail.com"
        self.mail_user = "tongshan1993@gmail.com"
        self.mail_pass = "shan84109649"

        self.sender = "tongshan1993@gmail.com"
        self.receivers = ["sara.tong@btcc.com"]
        self.message = MIMEText(Template.get_template(), 'html', 'utf-8')

        self.subject = get_time() + '测试报告'
        self.message['Subject'] = Header(self.subject, 'utf-8')

    def send(self):

        try:
            s = smtplib.SMTP_SSL(self.mail_host)
            s.login(self.mail_user, self.mail_pass)
            s.sendmail(self.sender, self.receivers, self.message.as_string())
            print("邮件发送成功")
            s.quit()
        except smtplib.SMTPException as e:
            print(e)
            print("Error: 无法发送邮件")


def get_time():
    return time.strftime('%Y-%m-%d', time.localtime())


class Template:

    top = """
    <style type="text/css">
    table{
    width: 600px;
    border-style: solid;
    border-width: 1px;
    border-collapse: collapse;
    }
    table thead tr td{
    height: 30px;
    font-size:18px;
    font-weight: bold;
    border-style: solid;
    border-width: 1px;
    }
    table tbody tr td{
    height: 20px;
    border-style: solid;
    border-width: 1px;
    table
    </style>
    <table>
    <thead>
    <tr>
    <td>检查点</td>
    <td>结果</td>
    <td>备注</td>
    </tr>
    </thead>
    <tbody>
    """
    middle = """
    """

    one_result = """
    <tr>
    <td>%(message)s</td>
    <td>%(result)s</td>
    <td>%(note)s</td>
    </tr>
    """
    bottom = """
    </tbody>
    </table>
    """

    @classmethod
    def add_result(cls, message, result, note):
        cls.middle += cls.one_result % dict(
            message=message,
            result=result,
            note=note,
        )

    @classmethod
    def get_template(cls):
        return cls.top+cls.middle+cls.bottom


if __name__ == "__main__":
     s = SendEmail()
     s.send()