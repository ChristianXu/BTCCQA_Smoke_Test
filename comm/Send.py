__author__ = 'sara'

import smtplib
import time
from email.mime.text import MIMEText
from email.header import Header


class SendEmail:
    def __init__(self):

        self.mail_host = u"smtp.gmail.com"
        self.mail_user = u"tongshan1993@gmail.com"
        self.mail_pass = u"shan84109649"

        self.sender = u"tongshan1993@gmail.com"
        self.receivers = [u"sara.tong@btcc.com", "christian.xu@btcc.com"]
        self.message = MIMEText(Template.get_template(), 'html', 'utf-8')

        self.subject = get_time() + u'测试报告'
        self.message['Subject'] = Header(self.subject, 'utf-8')

    def send(self):

        try:
            s = smtplib.SMTP_SSL(self.mail_host)
            smtplib.SMTP("smtp.gmail.com", 587)
            s.login(self.mail_user, self.mail_pass)
            s.sendmail(self.sender, self.receivers, self.message.as_string())
            print(u"邮件发送成功")
            s.quit()
        except smtplib.SMTPException as e:
            print(e)
            print(u"Error: 无法发送邮件")


def get_time():
    return time.strftime('%Y-%m-%d', time.localtime())


class Template:

    html = """

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
    table tr td{
    height: 20px;
    border-style: solid;
    border-width: 1px;
    table
    </style>

    <table>
    %(content)s

    </table>
    """

    middle = """
    """

    info = """
    <thead>
    <tr>
    <td colspan="3">
    <span>
    网站: %(website)s <br/>
    浏览器: %(browser)s <br/>
    测试账号: %(user)s <br/>
    </span>
    </td>
    </tr>
    <tr>
    <td>检查点</td>
    <td>结果</td>
    <td>备注</td>
    </tr>
    </thead>
    """

    one_result = """
    <tr>
    <td>%(message)s</td>
    <td>%(result)s</td>
    <td>%(note)s</td>
    </tr>
    """

    @classmethod
    def set_info(cls, website, browser, email):
        cls.info = cls.info % dict(
            website=website,
            browser=browser,
            user=email,
        )
        cls.middle += cls.info

    @classmethod
    def add_result(cls, message, result, note):

        cls.middle += cls.one_result % dict(
            message=message,
            result=result,
            note=note,
        )

    @classmethod
    def get_template(cls):
        return cls.html % dict(
            content=cls.middle
        )

    @classmethod
    def set_middle(cls, middle):
        cls.middle += middle


