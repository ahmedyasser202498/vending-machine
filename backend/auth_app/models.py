from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
import os
import ast

coins_str = os.environ.get('VALID_COINS')
valid_coins = ast.literal_eval(coins_str) 

class User(AbstractUser):
    ROLE_CHOICES = (('seller', 'Seller'), ('buyer', 'Buyer'))
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    deposit = models.PositiveIntegerField(default=0)
