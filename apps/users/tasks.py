# from myproject.celery import app
# from django.core.mail import send_mail
# from django.conf import settings
# <!-- http://{{ domain }}{% url 'users:activate' uidb64=uid token=token %} -->
# @app.task
# def send_message_to_email(email):
#     message = f"""Добро пожаловать в SAY-OPT-SHOP 
#     Вы получили это письмо, потому что пользователь {email} указал ваш e-mail для подключения 
#     к своему аккаунту.
#     Чтобы подтвердить, перейдите по ссылке {"http:://('api/v1/email-verify/')" + email +'/'}"""
#     send_mail(
#         "Пожалуйста подтвердите ваш e-mail адрес",
#         message, settings.EMAIL_HOST_USER,
#         [email],
#         fail_silently=False
#     )
#     return 'Send email verification'
