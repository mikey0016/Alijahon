from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.db.models import CharField, DecimalField, Model, CASCADE, ForeignKey, ImageField, TextField, DateTimeField, \
    IntegerField, SlugField, TextChoices


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
    api_key = CharField(max_length=255, null=True, blank=True)
    created_at = DateTimeField(auto_now_add=True)
    password = CharField(max_length=255, null=True, blank=True)

    first_name = CharField(max_length=100)
    last_name = CharField(max_length=100)
    telegram_id = CharField(max_length=50, null=True, blank=True , default="")
    description = TextField(null=True, blank=True , default="")

    referred_by = ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='referrals'
    )

class Transaction(Model):
    class TransactionType(TextChoices):
        MONEY = 'money' , 'Money'
        COIN = 'coin' , 'Coin'

    class TransactionStatus(TextChoices):
        PENDING = 'pending' , 'Pending'
        SUCCESS = 'success' , 'Success'
        REJECTED = 'rejected' , 'Rejected'

    user = ForeignKey('apps.User', on_delete=CASCADE, related_name='transactions')
    card_number = CharField(max_length=16)
    amount = DecimalField(max_digits=10, decimal_places=0)
    type = CharField(max_length=10, choices=TransactionType.choices, default=TransactionType.MONEY)
    status = CharField(max_length=10, choices=TransactionStatus.choices, default=TransactionStatus.PENDING)
    created_at = DateTimeField(auto_now_add=True)


class Category(Model):
    title = CharField(max_length=255)
    image = ImageField(upload_to='products/')


class Product(Model):
    title = CharField(max_length=50)
    price = DecimalField(max_digits=10, decimal_places=0)
    category = ForeignKey('apps.Category', on_delete=CASCADE, related_name='products')
    description = TextField()
    amount = IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = ImageField(upload_to='products/')
    discount = DecimalField(max_digits=10,decimal_places=0,default=0.0)

class Order(Model):
    first_name = CharField(max_length=50)
    phone_number = CharField(max_length=20)
    product_amount = DecimalField(max_digits=10, decimal_places=0)
    product = ForeignKey('apps.Product', on_delete=CASCADE, related_name='product_orders')
    user = ForeignKey('apps.User', on_delete=CASCADE, related_name='user_orders')
    created_at = DateTimeField(auto_now_add=True)


class Stream(Model):
    amount = IntegerField(blank=True, null=True)
    title = CharField(max_length=255)
    discount = DecimalField(max_digits=10, decimal_places=0, default=0)
    product = ForeignKey('apps.Product', on_delete=CASCADE, related_name='streams')
    user = ForeignKey('apps.User', on_delete=CASCADE, related_name='user_streams')
    created_at = DateTimeField(auto_now_add=True)

    visit = IntegerField(default=0)
    new_order = IntegerField(default=0)
    packing = IntegerField(default=0)
    delivering = IntegerField(default=0)
    delivered = IntegerField(default=0)
    waiting =  IntegerField(default=0)
    returned = IntegerField(default=0)
    cancelled = IntegerField(default=0)
    hold = IntegerField(default=0)
    archived = IntegerField(default=0)

# class Image(Model):
#     product = ForeignKey('apps.Product', on_delete=CASCADE, related_name='images')
#     product_image = ImageField(upload_to='products/')

class District(Model):
    title = CharField(max_length=255)