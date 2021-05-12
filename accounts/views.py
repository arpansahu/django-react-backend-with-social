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
from .models import NewUser
from .serializers import CustomUserSerializer, UserDetailsSerializer, ChangePasswordSerializer, UpdateUserSerializer, \
    ActivateAccount, ForgetPassword, ResetPassword
from rest_framework.permissions import AllowAny
import smtplib

from .token import account_activation_token, password_reset_token

sender_email = "developmenthai95@gmail.com"
password = "Tonystark302@"


def send_mail_account_activate(reciever_email, user, SUBJECT="Activate Your Account"):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    message = render_to_string(template_name='account/activate_account_mail.html', context={
        'user': user,
        'protocol': 'http',
        'domain': 'www.localhost:3000/activate',
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, reciever_email, message)


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
            print(serializer.data['uidb64'], serializer.data['token'])
            try:
                uid = force_text(urlsafe_base64_decode(serializer.data['uidb64']))
                user = NewUser.objects.get(pk=uid)
                print(uid, user)

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
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    message = render_to_string(template_name='account/password_reset_mail.html', context={
        'user': user,
        'protocol': 'http',
        'domain': 'www.localhost:3000/reset',
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': password_reset_token.make_token(user),
    })

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, reciever_email, message)


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
