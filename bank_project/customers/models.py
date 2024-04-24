from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
# Create your models here.

class CustomerManager(BaseUserManager):
    def _create_user(self, email, password, first_name, last_name, phonenumber, **extra_fields):
        if not email:
            raise ValueError('Email is not provided')
        if not password:
            raise ValueError('Password is not provided')
        
        customer = self.model(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            phonenumber = phonenumber,
            **extra_fields
        )

        customer.set_password(password)
        customer.save(using=self.db)
        return customer
    
    def create_user(self, email, password, first_name, last_name, phonenumber, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, first_name, last_name, phonenumber, password, **extra_fields)
    
    def create_superuser(self, email, password, first_name, last_name, phonenumber, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, first_name, last_name, phonenumber, **extra_fields)
    

class Customer(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, max_length=200)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phonenumber = models.CharField(unique=True, max_length=100)
    account_number = models.CharField(max_length=20)
    account_balance = models.FloatField(default=0)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)

    objects = CustomerManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phonenumber']

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'


class Transfer(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    receiver_account = models.CharField(max_length=20)
    amount = models.IntegerField()
    date = models.DateTimeField(default=timezone.now)
    def __repr__(self):
        return f'''{self.sender}, {self.amount}, {self.date}'''