# import logging
 
# from django.urls import reverse
# from django.core.mail import EmailMessage
# from django.contrib.auth import get_user_model
# from thisblog.celery import app
 
 
# @app.task
# def send_email_to_user(user_id, mail_subject, message, to_email):
#     UserModel = get_user_model()
#     try:        
#         try:
#             email = EmailMessage(mail_subject, message, to=[to_email])
#             email.send()
#         except email is None:
#             logging.warning("Tried to send an invalid email")    

#     except UserModel.DoesNotExist:
#         logging.warning("Tried to send email to non-existing user '%s'" % user_id)