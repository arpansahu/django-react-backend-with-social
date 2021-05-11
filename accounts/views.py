import json

from django.http import JsonResponse
from rest_framework.exceptions import ErrorDetail
from rest_framework import status, permissions
from rest_framework.generics import UpdateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import NewUser
from .serializers import CustomUserSerializer, UserDetailsSerializer, ChangePasswordSerializer, UpdateUserSerializer
from rest_framework.permissions import AllowAny


class CustomUserCreate(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format='json'):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            # print("IS VALID")
            user = serializer.save()

            if user:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        if dict(serializer.errors)[list(serializer.errors.keys())[0]] == [ErrorDetail(string='The fields email must make a unique set.', code='unique')]:
            return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)
        else:
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
