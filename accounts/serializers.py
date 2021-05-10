from rest_framework import serializers
from rest_framework.fields import CharField
from rest_framework.views import APIView

from accounts.models import NewUser


# from rest_framework.validators import UniqueTogetherValidator


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Currently unused in preference of the below.
    """
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = NewUser
        fields = ('email', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=NewUser.objects.all(),
        #         fields=['email']
        #     )
        # ]

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        # as long as the fields are the same, we can just use this
        instance = self.Meta.model(**validated_data)
        print(instance.email)
        if NewUser.objects.get(email=instance.email):
            print("user reg")
            return serializers.ErrorDetail("User Account Already Exists")
        else:
            if password is not None:
                instance.set_password(password)
                instance.is_active = True
            instance.save()
            return instance


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = ('email', 'username', 'first_name', 'about', 'is_staff', 'is_active')


class UserUpdateSerializer(serializers.ModelSerializer):
    email = CharField(max_length=30,  required=False)
    about = CharField(max_length=3000, required=False)
    password = CharField(max_length=30, required=False)
    username = CharField(max_length=30,  required=False)

    class Meta:
        model = NewUser
        fields = ('email', 'username', 'about', 'password')
