import json
import ssl

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from rest_framework.exceptions import ErrorDetail
from rest_framework import status, permissions
from rest_framework.generics import UpdateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.encoding import force_bytes

from core.settings import SMTP_SERVER, SMTP_PORT, SMTP_PASSWORD, SMTP_EMAIL, DOMAIN
from .models import NewUser
from .serializers import CustomUserSerializer, UserDetailsSerializer, ChangePasswordSerializer, UpdateUserSerializer, \
    ActivateAccount, ForgetPassword, ResetPassword
from rest_framework.permissions import AllowAny

from .token import account_activation_token, password_reset_token
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# def send_mail_account_activate(reciever_email, user, SUBJECT="Activate Your Account"):
#     port = 465  # For SSL
#     smtp_server = "smtp.gmail.com"
#     # message = render_to_string(template_name='account/activate_account_mail.html', context={
#     #     'user': user,
#     #     'protocol': 'http',
#     #     'domain': 'www.localhost:3000/activate',
#     #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#     #     'token': account_activation_token.make_token(user),
#     # })
#
#     # context = ssl.create_default_context()
#     message = MIMEMultipart()
#     message["Subject"] = "Accoutn Activation Email"
#     message["From"] = sender_email
#     message["To"] = reciever_email
#
#     text = """
#     <!DOCTYPE html>
#         <head>
#             <style>
#                 h1{position:absolute;text-align: center;}
#                 img{width:100%;}
#                 .container {
#                                 position: relative;
#                                 text-align: center;
#                             }
#                 .centered {
#                                 position: absolute;
#                                 z-index: 999;
#                                 margin: 0 auto;
#                                 left: 0;
#                                 right: 0;
#                                 top: 40%;
#                                 text-align: center;
#                                 width: 60%;
#                             }
#                 body{
#                                 background-color:blue;
#                                 background-repeat:no-repeat;
#                 }
#             </style>
#         </head>
#         """ + """
#         <body>
#             <h1>Hello {0}</h1>
#             <br/>
#             <div class ="container">
#
#                 <div class="centered">
#                     <p>
#                         To initiate the account acctivation process for your account on {{ domain }},
#                         click the link below:
#                         <br><br>
#                         <a href="http://localhost:3000/{1}/{2}">Activate Your account here</a>
#                         <br><br>
#                         If clicking the link above doesn't work, please copy and paste the URL in a new browser
#                         window instead.
#                     </p>
#                 </div>
#             </div>
#
#             <br/>
#         </body>
#         </html>
#     """.format(reciever_email, urlsafe_base64_encode(force_bytes(user.pk)), account_activation_token.make_token(user))
#     part = MIMEText(text, "html")
#     message.attach(part)
#     with smtplib.SMTP_SSL(smtp_server, port) as server:
#         server.login(sender_email, password)
#         server.sendmail(sender_email, reciever_email, message)

def send_mail_account_activate(reciever_email, user, SUBJECT="Activate Your Account"):
    port = 465
    smtp_server = SMTP_SERVER
    message = render_to_string(template_name='account/activate_account_mail.html', context={
        'user': user,
        'protocol': 'http',
        'domain': DOMAIN + '/activate',
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(SMTP_EMAIL, SMTP_PASSWORD)
        server.sendmail(SMTP_EMAIL, reciever_email, message)
    print("account activation mail send")


# class CustomUserCreate(APIView):
#     permission_classes = [AllowAny]
#
#     def post(self, request, format='json'):
#         serializer = CustomUserSerializer(data=request.data)
#         if serializer.is_valid():
#             # print("IS VALID")
#             user = serializer.save()
#
#             if user:
#                 json = serializer.data
#                 send_mail_account_activate(serializer.email, user)
#                 return Response(json, status=status.HTTP_201_CREATED)
#         print(serializer.errors)
#         if dict(serializer.errors)[list(serializer.errors.keys())[0]] == [
#             ErrorDetail(string='The fields email must make a unique set.', code='unique')]:
#             return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomUserCreate(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format='json'):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                json = serializer.data
                print(user.email, user)
                send_mail_account_activate(user.email, user)
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountDetails(RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = [UserDetailsSerializer]

    def get(self, request, *args, **kwargs):
        # print(request.user)
        ser = UserDetailsSerializer(request.user)
        return Response(ser.data)


class ChangePasswordView(UpdateAPIView):
    queryset = NewUser.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ChangePasswordSerializer


class UpdateProfileView(UpdateAPIView):
    queryset = NewUser.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UpdateUserSerializer


class AccountActivateView(APIView):
    serializer_class = ActivateAccount

    def post(self, request, *args, **kwargs):
        serializer = ActivateAccount(data=request.data)
        if serializer.is_valid():
            # print(serializer.data['uidb64'], serializer.data['token'])
            try:
                uid = force_text(urlsafe_base64_decode(serializer.data['uidb64']))
                user = NewUser.objects.get(pk=uid)
                # print(uid, user)

            except (TypeError, ValueError, OverflowError, NewUser.DoesNotExist) as e:
                user = None

            if user is not None and account_activation_token.check_token(user, serializer.data['token']):
                if user.is_email_verified:
                    return Response("Account Verified Already", status=status.HTTP_202_ACCEPTED)
                user.is_email_verified = True  # now we're activating the user
                # user.profile.email_confirmed = True  # and we're changing the boolean field so that the token link
                # becomes invalid
                user.save()
                # login(request, user)  # log the user in
                return Response("Account Verified Successfully", status=status.HTTP_202_ACCEPTED)
            else:
                return Response("Activation link expired activated", status=status.HTTP_403_FORBIDDEN)
        return Response("Account Activated")


def send_mail_password_reset(reciever_email, user, SUBJECT="Activate Your Account"):
    port = SMTP_PORT  # For SSL
    smtp_server = SMTP_SERVER
    message = render_to_string(template_name='account/password_reset_mail.html', context={
        'user': user,
        'protocol': 'http',
        'domain': DOMAIN + '/reset',
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': password_reset_token.make_token(user),
    })

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(SMTP_EMAIL, SMTP_PASSWORD)
        server.sendmail(SMTP_EMAIL, reciever_email, message)


class ForgetPasswordView(APIView):
    serializer_class = ForgetPassword

    def post(self, request, *args, **kwargs):
        serializer = ForgetPassword(data=request.data)
        if serializer.is_valid():
            try:
                user = NewUser.objects.get(email=serializer.data['email'])
            except Exception as e:
                if e.args[0] == "NewUser matching query does not exist.":
                    return Response("Account not found with this email", status=status.HTTP_404_NOT_FOUND)
                print(e)
            # print(user, user.email)
            send_mail_password_reset(user.email, user)
            return Response("Password Reset Email is Send Scuessfully", status=status.HTTP_200_OK)


class ResetPasswordView(APIView):
    serializer_class = ResetPassword

    def post(self, request, *args, **kwargs):
        serializer = ResetPassword(data=request.data)
        if serializer.is_valid():
            print(serializer.data['uidb64'], serializer.data['token'], serializer.data['password1'],
                  serializer.data['password2'])
            try:
                uid = force_text(urlsafe_base64_decode(serializer.data['uidb64']))
                user = NewUser.objects.get(pk=uid)
                print("this iss it\n", uid, user)

            except (TypeError, ValueError, OverflowError, NewUser.DoesNotExist) as e:
                user = None

            if user is not None and account_activation_token.check_token(user, serializer.data['token']):
                if serializer.data['password1'] == serializer.data['password2']:
                    user.set_password(serializer.data['password2'])
                    user.save()
                    return Response("Password Reset Successfully", status=status.HTTP_202_ACCEPTED)

                return Response("Both passwords do not match", status=status.HTTP_206_PARTIAL_CONTENT)
            else:
                return Response("Activation link expired activated", status=status.HTTP_403_FORBIDDEN)
        return Response("Password Reset Successfully")
