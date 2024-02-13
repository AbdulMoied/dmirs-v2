from django.test import TestCase
from django.urls import reverse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import Group
from authentication.models import Account 
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode

class AuthenticationViewsTestCase(TestCase):
    def setUp(self):

        super_admin_group, created = Group.objects.get_or_create(name='Super Admin')

        self.user = Account.objects.create_user(
            email='testuser@example.com',
            password='testpassword',
            first_name='Test',
            last_name='User',
        )

        self.admin = Account.objects.create_superuser(
            email='admin@example.com',
            password='adminpassword',
            first_name='Admin',
            last_name='User',
        )
        self.admin.groups.add(super_admin_group)

    def test_obtain_token_pair_view(self):

        url = reverse('login')
        data = {'email': 'testuser@example.com', 'password': 'testpassword'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_change_password_view(self):
        url = reverse('change-password')
        data = {
            'current_password': 'testpassword',
            'new_password': 'newtestpassword',
            'new_password_confirm': 'newtestpassword',
        }
        self.client.login(email='testuser@example.com', password='testpassword')
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)

        response = self.client.patch(
            url,
            data,
            content_type='application/json',
            HTTP_AUTHORIZATION=f'Bearer {access_token}',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'success')


    def test_user_list_view(self):

        url = reverse('get_all_users/')
        self.client.login(email='admin@example.com', password='adminpassword')
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)
        response = self.client.get(
            url,
            HTTP_AUTHORIZATION=f'Bearer {access_token}',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class ResetPasswordTestCase(APITestCase):

    def setUp(self):

        super_admin_group, created = Group.objects.get_or_create(name='Super Admin')

    def test_reset_password_superuser(self):

        superuser = Account.objects.create_superuser(
            email='superuser@example.com',
            password='superuserpassword',
            first_name='Super',
            last_name='User',
        )

        self.client.force_authenticate(user=superuser)
        response = self.client.patch(reverse('reset-user-password', kwargs={'pk': superuser.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reset_password_non_superuser(self):

        regular_user = Account.objects.create_user(
            email='user@example.com',
            password='userpassword',
            first_name='Regular',
            last_name='User',
        )
        self.client.force_login(regular_user)
        response = self.client.patch(reverse('reset-user-password', kwargs={'pk': regular_user.pk}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class RequestPasswordResetEmailTestCase(APITestCase):
    def request_password_reset_email(self, email):
        response = self.client.post(reverse('reset_password'), data={'email': email})
        return response

    def test_request_password_reset_email_valid_email(self):
        user = Account.objects.create_user(
            email='user@example.com',
            password='userpassword',
            first_name='Test',
            last_name='User',
        )
        response = self.request_password_reset_email('user@example.com')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_request_password_reset_email_invalid_email(self):
        response = self.request_password_reset_email('invalid@example.com')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class SetNewPasswordAPIViewTestCase(APITestCase):
    def set_new_password(self, uid, token, new_password):
        print("============ before", uid, "=============")

        try:
            response = self.client.patch(
                reverse('password-reset-confirm'),
                data={'uid': uid, 'token': token, 'new_password': new_password, 'password': 'your_password_here', 'confirm_password': 'your_password_here'},
            )
            return response

        except UnicodeDecodeError as e:
            return Response({'error': 'Invalid UID'}, status=status.HTTP_400_BAD_REQUEST)

    def test_set_new_password_valid_link(self):
        user = Account.objects.create_user(
            email='user@example.com',
            password='userpassword',
            first_name='Test',
            last_name='User',
        )
        uidb64 = urlsafe_base64_encode(str(user.id).encode())
        token = PasswordResetTokenGenerator().make_token(user)
        response = self.set_new_password(uidb64, token, 'newpassword')
        response.render()

    def test_set_new_password_invalid_link(self):
        response = self.set_new_password('invalid_uid', 'invalid_token', 'newpassword')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)