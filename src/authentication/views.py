"Authentication Views"
from authentication.models import Account
from authentication.serializers import ChangePasswordSerializer, CustomTokenObtainPairSerializer,ResetPasswordEmailRequestSerializer,SetNewPasswordSerializer
from authentication.utils import send_reset_password_email

from rest_framework import permissions, status, generics
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response

from rest_framework.decorators import action
from rest_framework import viewsets
from django.contrib.auth.models import Permission
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import smart_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny
from authentication.serializers import AccountListSerializer
from backend_main.constants import screens,actions
# from backend_main.permissions import UserPermissions
import copy
from django.db.models import Q
from .utils import get_portal_permissions

from threading import Thread
from backend_main.utils import send_mail_to_user

from drf_yasg.utils import swagger_auto_schema
from django.utils.decorators import method_decorator


@method_decorator(
    name='post', decorator=swagger_auto_schema(
    operation_summary="Get token from email and password",operation_description="This endpoint returns token after entering email and password")
) 
class ObtainTokenPairView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = CustomTokenObtainPairSerializer

@method_decorator(
    name='put', decorator=swagger_auto_schema(
    operation_summary="Update User's password",operation_description="This endpoint updates User's password")
) 
@method_decorator(
    name='patch', decorator=swagger_auto_schema(
    operation_summary="Update User's password",operation_description="This endpoint updates User's password")
) 
class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """

    serializer_class = ChangePasswordSerializer
    model = Account
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("current_password")):
                return Response(
                    {"message": ["Current password is Invalid."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # check if both password matches
            if serializer.data.get("new_password") != serializer.data.get(
                "new_password_confirm"
            ):
                return Response(
                    {"message": "Password not match"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            else:
                # set_password also hashes the password that the user will get
                self.object.set_password(serializer.data.get("new_password"))
                self.object.save()
                response = {
                    "status": "success",
                    "code": status.HTTP_200_OK,
                    "message": "Password updated successfully",
                }
                return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_permissions(request):
    #Right now we don't need to do this because only one type of user can login(Superuser who has admin group so giving Admin permissions to view all screens and perform all actions.)

    # # Get all the permissions from the auth.Permission model
    permissions = Permission.objects.all()
    
    user_permissions = []


    get_portal_permissions(permissions,user_permissions,screens,actions)   
    

    return Response(data=user_permissions)


@method_decorator(
    name='get', decorator=swagger_auto_schema(
    operation_summary="Get list of all User object",operation_description="This endpoint returns list of all User object")
) 
class UserList(generics.ListAPIView):
    queryset = Account.objects.all().order_by('first_name')
    serializer_class = AccountListSerializer
    permission_classes = [IsAuthenticated]


@method_decorator(
    name='put', decorator=swagger_auto_schema(
    operation_summary="Update User's password and send new password in email",operation_description="This endpoint updates User's password and sends new password in email")
) 
@method_decorator(
    name='patch', decorator=swagger_auto_schema(
    operation_summary="Update User's password and send new password in email",operation_description="This endpoint updates User's password and sends new password in email")
)
class ResetPassword(generics.UpdateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountListSerializer

    def update(self, request, *args, **kwargs):
        if request.user.is_superuser:
            user_id = kwargs['pk']
            user = Account.objects.get(id=user_id)
            password = Account.objects.make_random_password()
            user.set_password(password)
            user.save()

            # sending mail to user
            context = {"first_name":user.first_name,"email":user.email,"password":password}
            t = Thread(target=send_mail_to_user,args=(context,))
            t.start()
            return Response({'status': f'New Password sent to user {user.first_name} {user.last_name}'})
        else:
            return Response({'status': 'You do not have permission to perform this action'})
        

#Reset password implementation new requirements
@method_decorator(
    name='post', decorator=swagger_auto_schema(
    operation_summary="Get password reset link",operation_description="This endpoint returns password reset link")
)
class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer
    permission_classes = [AllowAny]

    def post(self,request):
        email = request.data.get('email', '')

        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            reset_password_link = f"{request.headers.get('Referer')}ConfirmPassword/{uidb64}/{token}"
            context = {'reset_password_link': reset_password_link, 'to_email': [user.email]}
            send_reset_password_email(context)
            return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)
        else:
            return Response({'Failed': 'Invalid Email, Please Enter Your Verified Email Address'}, status=status.HTTP_404_NOT_FOUND)
        
@method_decorator(
    name='patch', decorator=swagger_auto_schema(
    operation_summary="Reset password after clicking password reset link",operation_description="This endpoint resets password after clicking password reset link")
)        
class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    permission_classes = [AllowAny]


    def patch(self, request):
        uid = urlsafe_base64_decode(request.data.get('uid')).decode()
        user = Account.objects.filter(pk=uid).first()
        token = request.data.get('token',None)
        if not user:
            return Response({'Failed':'User Not Found'},status = status.HTTP_404_NOT_FOUND)
        if PasswordResetTokenGenerator().check_token(user, token):
            request.session['uid'] = uid
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            return Response({'success': True, 'message': 'Password Reset Successfully'}, status=status.HTTP_200_OK)
        return Response({'Failed': 'Link has been expired'}, status=status.HTTP_404_NOT_FOUND)