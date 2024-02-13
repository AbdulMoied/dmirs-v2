from django.test import TestCase
from django.contrib.auth.models import Group
from unittest.mock import patch
from authentication.models import Account

class AccountModelTestCase(TestCase):
    def setUp(self):
        # Create the 'Super Admin' group before each test
        Group.objects.get_or_create(name='Super Admin')

    def test_create_user(self):
        # Test creating a regular user
        user = Account.objects.create_user(
            email='user@example.com',
            password='testpassword',
            first_name='John',
            last_name='Doe',
        )
        self.assertEqual(user.email, 'user@example.com')
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    @patch('authentication.models.MyAccountManager.create_user')
    def test_create_staff(self, mock_create_user):
        # Mock the create_user method to capture the arguments
        mock_create_user.return_value = Account(email='staff@example.com', is_staff=True)

        # Test creating a staff user
        staff_user = Account.objects.create_staff(
            email='staff@example.com',
            password='testpassword',
            first_name='Staff',
            last_name='Member',
        )

        # Assert that create_user was called with the correct arguments
        mock_create_user.assert_called_once_with(
            email='staff@example.com',
            password='testpassword',  # Pass the password here
            first_name='Staff',
            last_name='Member',
        )

        self.assertEqual(staff_user.email, 'staff@example.com')
        self.assertTrue(staff_user.is_staff)
        self.assertFalse(staff_user.is_superuser)
        self.assertTrue(Account.objects.filter(email='staff@example.com').exists())

    def test_create_superuser(self):
        # Test creating a superuser
        superuser = Account.objects.create_superuser(
            email='admin@example.com',
            password='testpassword',
            first_name='Admin',
            last_name='User',
        )
        self.assertEqual(superuser.email, 'admin@example.com')
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(Account.objects.filter(email='admin@example.com').exists())
        self.assertTrue(superuser.groups.filter(name='Super Admin').exists())

    def test_superuser_has_group(self):
        # Test if superuser is assigned to the 'Super Admin' group
        superuser = Account.objects.create_superuser(
            email='admin@example.com',
            password='testpassword',
            first_name='Admin',
            last_name='User',
        )
        self.assertTrue(superuser.groups.filter(name='Super Admin').exists())
