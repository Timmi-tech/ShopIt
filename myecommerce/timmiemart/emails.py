from django.conf import settings
from django.core.mail import send_mail

def send_account_activation_email(email, email_token):
    subject = 'Your account needs to be verified'
    email_from = settings.EMAIL_HOST_USER
    message = f'Hi, click on the link to activate your accounthttp://127.0.0.1:8000/activate/{email_token}'


    send_mail(subject, email_from, {email})