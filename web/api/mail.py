# 寄信module
from django.core.mail import EmailMultiAlternatives
from email.mime.image import MIMEImage


def send_mail(subject, text):
    """
    寄信功能
    """
    from_email = '3CP@conquers.co'
    text_content = f'''
    {text}        
    '''

    msg = EmailMultiAlternatives(subject, text_content, from_email, ['3CP@conquers.co'])
    msg.attach_alternative(text_content, "text/html")

    msg.send()
