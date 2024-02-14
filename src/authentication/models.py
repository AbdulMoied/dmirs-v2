from django.db import models
from django.contrib.auth.models import Group

from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)



class MyAccountManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email, password and username.
        """
        if not email:
            raise ValueError("Users must have an email address!")

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staff(self, email, password, **extra_fields):
        """
        Create and save a User with the given email, password and username.
        """
        if not email:
            raise ValueError("Staff must have an email address!")

        email = self.normalize_email(email)

        user = self.create_user(
            email=email,
            password=password,
            **extra_fields,
        )
        user.is_staff = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            **extra_fields,
        )

        user.is_active = True
        user.is_staff = True
        user.is_superuser = True

        admin_group = Group.objects.get(name='Super Admin')
        user.groups.add(admin_group)
        print(f'Assigned {admin_group} to user {user}')

        user.save(using=self._db)

        return user


class Account(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(verbose_name="first name", max_length=20)
    last_name = models.CharField(verbose_name="last name", max_length=20)
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = MyAccountManager()
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return self.email

    def get_short_name(self):
        return self.USERNAME_FIELD