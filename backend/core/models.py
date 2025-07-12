from django.db import models
from auth_app.models import User
from django.core.exceptions import ValidationError

class Product(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    product_name = models.CharField(max_length=100)
    cost = models.PositiveIntegerField()
    amount_available = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        if self.cost % 5 != 0:
            raise ValidationError({'cost': 'Cost must be divisible by 5.'})
        return super().save(*args, **kwargs)