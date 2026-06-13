from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.auth.hashers import make_password
from django.db import models
from django.db.models import Model, ForeignKey, CASCADE, TextField,IntegerField, CharField, DecimalField, DateTimeField, ImageField



class CustomUserManager(UserManager):
    def _create_user(self, phone_number, password, **extra_fields):
        if not phone_number:
            raise ValueError("Telefon raqam kiritilishi shart!")
        user = self.model(phone_number=phone_number, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(phone_number, password, **extra_fields)

    def create_superuser(self, phone_number=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
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
    telegram_id = CharField(max_length=50, null=True, blank=True, default="")
    description = TextField(null=True, blank=True, default="")
    referred_by = ForeignKey('self', on_delete=CASCADE ,null=True, blank=True, related_name='referrals')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Transaction(Model):
    TYPE_CHOICES = [('money', 'Money'), ('coin', 'Coin')]
    STATUS_CHOICES = [('pending', 'Pending'), ('success', 'Success'), ('rejected', 'Rejected')]

    user = ForeignKey(User, CASCADE, related_name='transactions')
    card_number = CharField(max_length=16)
    amount = DecimalField(max_digits=10, decimal_places=0)
    type = CharField(max_length=10, choices=TYPE_CHOICES, default='money')
    status = CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.phone_number} - {self.amount}"


class Category(Model):
    title = CharField(max_length=255)
    image = ImageField(upload_to='products/')

    def __str__(self):
        return self.title


class Product(Model):
    title = CharField(max_length=50)
    price = DecimalField(max_digits=10, decimal_places=0)
    category = ForeignKey(Category, CASCADE, related_name='products')
    description = TextField()
    amount = IntegerField()
    image = ImageField(upload_to='products/')
    created_at = DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Order(Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'), ('waiting', 'Waiting'),
        ('delivering', 'Delivering'), ('delivered', 'Delivered'), ('cancelled', 'Cancelled'),
    ]

    product = ForeignKey(Product, CASCADE, null=True)
    full_name = CharField(max_length=100)
    phone_number = CharField(max_length=20)
    quantity = IntegerField()
    total_price = IntegerField()
    status = CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.full_name}"


class Stream(Model):
    title = CharField(max_length=255)
    amount = IntegerField(blank=True, null=True)
    discount = DecimalField(max_digits=10, decimal_places=0, default=0)
    product = ForeignKey(Product, CASCADE, related_name='streams')
    user = ForeignKey(User, CASCADE, related_name='user_streams')
    created_at = DateTimeField(auto_now_add=True)

    visit = 0
    new_order = 0
    packing = 0
    delivering = 0
    delivered = 0
    waiting = 0
    returned = 0
    cancelled = 0
    hold = 0
    archived = 0

    def __str__(self):
        return f"{self.title} - {self.user.phone_number}"


class District(Model):
    title = CharField(max_length=255)

    def __str__(self):
        return self.title


class WishList(Model):
    user = ForeignKey(User, CASCADE, related_name='wishlists')
    product = ForeignKey(Product, CASCADE, related_name='wishlists')
    created_at = DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.phone_number} - {self.product.title}"