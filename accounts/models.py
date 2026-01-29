class ClientManager(CustomUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(role='client')

class EmployeeManager(CustomUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(role='staff')

# Proxy models for admin split
class Client(CustomUser):
    objects = ClientManager()
    class Meta:
        proxy = True
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'

class Employee(CustomUser):
    objects = EmployeeManager()
    class Meta:
        proxy = True
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone

# ClientFile model for client document management
class ClientFile(models.Model):
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='client_files')
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='uploaded_files')
    file = models.FileField(upload_to='client_files/')
    description = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.file.name} for {self.client.get_full_name()}"

    class Meta:
        app_label = 'accounts'

class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, first_name, last_name, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('client', 'Client'),
        ('staff', 'Staff/Employee'),
    )

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    # Profile fields
    picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    phone_number_1 = models.CharField(max_length=32, blank=True)
    phone_number_2 = models.CharField(max_length=32, blank=True)
    address_1 = models.CharField(max_length=255, blank=True)
    address_2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=64, blank=True)
    state = models.CharField(max_length=32, blank=True)
    zip_code = models.CharField(max_length=16, blank=True)
    company_role = models.CharField(max_length=64, blank=True, help_text="Job title or company role")
    bio = models.TextField(blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='client')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    class Meta:
        app_label = 'accounts'

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name} <{self.email}>"
