from multiprocessing import Process
from django.core.mail import send_mail
from django.conf import settings

def send_verification_email(email, otp):
    send_mail(
        'Verify Your Email',
        f'Your verification code is: {otp}',
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=True,
    )
