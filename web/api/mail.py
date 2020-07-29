# 寄信module
from django.core.mail import EmailMultiAlternatives
from email.mime.image import MIMEImage


def send_mail(subject, text):
    """
    寄信功能
    :param subject: 主題
    :param text: 內容
    :return:
    """
    # 來源
    from_email = '3CP@conquers.co'
    text_content = f'''
    {text}        
    '''

    # 寄信寫法
    msg = EmailMultiAlternatives(subject, text_content, from_email, ['3CP@conquers.co'])
    msg.attach_alternative(text_content, "text/html")
    msg.send()
