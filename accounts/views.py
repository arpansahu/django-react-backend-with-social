import json

from django.http import JsonResponse
from rest_framework.exceptions import ErrorDetail
from rest_framework import status, permissions, viewsets
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import NewUser
from .serializers import CustomUserSerializer, UserDetailsSerializer, UserUpdateSerializer
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
        if dict(serializer.errors)[list(serializer.errors.keys())[0]] == [
            ErrorDetail(string='The fields email must make a unique set.', code='unique')]:
            return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountDetails(RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # print(request.user)
        ser = UserDetailsSerializer(request.user)
        return Response(ser.data)

    def patch(self, request, *args, **kwargs):
        print("inside patch")
        user = NewUser.objects.get(email=request.user)
        serializer = UserUpdateSerializer(user, data=request.data)  # set partial=True to update a data partially
        print("after serializer")
        if serializer.is_valid():
            print(serializer)
            # serializer.save()
            serializer.update(user, validated_data=request.data)
            print(serializer.data)
            # user.username = serializer.data['username']
            print("SuccessFull")
            return Response( status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
