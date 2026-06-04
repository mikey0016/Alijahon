from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.db.models import CharField, DecimalField, Model, CASCADE, ForeignKey, ImageField, TextField, DateTimeField, \
    IntegerField, SlugField


class CustomUserManager(UserManager):

    def _create_user_object(self, phone_number, password, **extra_fields):
        if not phone_number:
            raise ValueError("The given phone must be set")
        user = self.model(phone_number=phone_number, **extra_fields)
        user.password = make_password(password)
        return user

    def _create_user(self, phone_number, password, **extra_fields):
        """
        Create and save a user with the given  phone_number, and password.
        """
        user = self._create_user_object(phone_number, password, **extra_fields)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(phone_number, password, **extra_fields)

    def create_superuser(self, phone_number=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(phone_number, password, **extra_fields)


class User(AbstractUser):
    username = None
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()
    phone_number = CharField(unique=True, max_length=20)
    balance = DecimalField(max_digits=10, decimal_places=0, default=0)
    coins = DecimalField(max_digits=10, decimal_places=0, default=0)
    api_key = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    password = models.CharField(max_length=255, null=True, blank=True)
    conf_password = models.CharField(max_length=255, null=True, blank=True)


class Category(Model):
    title = CharField(max_length=255)
    photo = ImageField(upload_to='products/')


class Product(Model):
    title = CharField(max_length=50)
    price = DecimalField(max_digits=10, decimal_places=0)
    category = ForeignKey('apps.Category', on_delete=CASCADE, related_name='products')
    description = TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = ImageField(upload_to='products/')


class Order(Model):
    first_name = CharField(max_length=50)
    phone_number = CharField(max_length=20)
    product_amount = DecimalField(max_digits=10, decimal_places=0)
    product = ForeignKey('apps.Product', on_delete=CASCADE, related_name='product_orders')
    user = ForeignKey('apps.User', on_delete=CASCADE, related_name='user_orders')
    created_at = DateTimeField(auto_now_add=True)


# class Image(Model):
#     product = ForeignKey('apps.Product', on_delete=CASCADE, related_name='images')
#     product_image = ImageField(upload_to='products/')
