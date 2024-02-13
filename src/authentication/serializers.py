from authentication.models import Account

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed,NotAcceptable

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

from requests import request

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ("first_name", "last_name", "phone_number", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

class AccountListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = (
            "id",
            "first_name",
            "last_name",
            "phone_number",
            "email",
        )
        
class ChangePasswordSerializer(serializers.Serializer):
    model = Account

    """
    Serializer for password change endpoint.
    """

    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password_confirm = serializers.CharField(required=True)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(CustomTokenObtainPairSerializer, cls).get_token(user)
        # Add custom claims
        token["user"] = AccountSerializer(user, context={"request": request}).data
        user = Account.objects.filter(id = token["user_id"]).first()
        token["user_group"] =  user.groups.values_list('name',flat = True).first()
        return token


class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)


    class Meta:
        fields = ['email']


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    uid = serializers.CharField(
        min_length=1, write_only=True)
    token = serializers.CharField(
        min_length=1, write_only=True)
    

    class Meta:
        fields = ['password', 'confirm_password' ,'token', 'uid']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            confirm_password = attrs.get('confirm_password')
            token = attrs.get('token')
            uid = attrs.get('uid')
            
            id = force_str(urlsafe_base64_decode(uid))
            user = Account.objects.filter(id=id).first()
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)

            if password == confirm_password:
                user.set_password(password)
                user.save()
                return (user)
            else:
                raise NotAcceptable("Password doesn't match confirm password",406)

            
        except Exception as e:
            raise NotAcceptable("Password doesn't match confirm password",406)
            
        return super().validate(attrs)