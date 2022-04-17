from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserManager(BaseUserManager):

    def create_user(self, email, user_name, pitaji, mataji, password, **other_fields):
        if not email:
            raise ValueError('Email is required.')

        # email = email.normalize_email(email)
        user = self.model(email=email, user_name=user_name, pitaji=pitaji, mataji=mataji, **other_fields)
        user.set_password(password)
        user.save(self._db)

        return user

    def create_superuser(self, email, user_name, pitaji, mataji, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_superuser', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True.')

        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, user_name, pitaji, mataji, password, **other_fields)


class Manushya(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    user_name = models.CharField(max_length=100)
    gaon = models.CharField(max_length=100)
    pitaji = models.CharField(max_length=100)
    mataji = models.CharField(max_length=100)
    viradari = models.CharField(max_length=100)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name','pitaji', 'mataji']

    def __str__(self):
        return self.email


class HexString(models.Model):
    code = models.CharField(max_length=30, blank=False, unique=True)
    manushya = models.ForeignKey(Manushya, on_delete=models.CASCADE)
    generated_at = models.DateTimeField(auto_now=True)
