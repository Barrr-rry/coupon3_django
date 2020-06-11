from django.core.mail import EmailMultiAlternatives
from email.mime.image import MIMEImage


def send_mail(subject, tomail, text):
    from_email = 'Ezgobuyusa@gmail.com'
    text_content = f'''
    {text}        
    '''

    msg = EmailMultiAlternatives(subject, text_content, from_email, [tomail])
    msg.attach_alternative(text_content, "text/html")

    msg.send()
