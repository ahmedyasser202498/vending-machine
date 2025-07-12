from rest_framework.response import Response
from rest_framework import status
import os
import ast
from rest_framework.exceptions import ValidationError, NotFound, PermissionDenied

from .models import Product
import logging

logger = logging.getLogger(__name__)


class CoreService:
    def __init__(self):
        coins_str = os.environ.get('VALID_COINS')
        self.valid_coins = ast.literal_eval(coins_str) 
    
    def handle_deposit(self,user, amount):
        logger.info(f"{user.username} attempts to deposit {amount}")

        if amount not in self.valid_coins:
            logger.warning(f"Invalid deposit amount: {amount} by user {user.username}")
            raise ValueError('Invalid coin')

        user.deposit += amount
        user.save()

        logger.info(f"{user.username} deposit updated to {user.deposit}")
        return user.deposit


    def handle_reset(user):
        logger.info(f"{user.username} is resetting deposit")
        user.deposit = 0
        user.save()
        
        return user.deposit

    def handle_buy(self,user,product_id,quantity):
        logger.info(f"{user.username} is buying product {product_id} (qty: {quantity})")

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            logger.error(f"Product {product_id} not found")
            raise NotFound('Product not found')

        total_cost = product.cost * quantity

        if user.deposit < total_cost:
            logger.warning(f"{user.username} has insufficient deposit for purchase")
            raise PermissionDenied('Insufficient deposit')

        if product.amount_available < quantity:
            logger.warning(f"Product {product.product_name} not enough in stock")
            raise ValidationError('Not enough product stock')

        product.amount_available -= quantity
        product.save()

        user.deposit -= total_cost
        change = user.deposit
        coin_change = {}

        for coin in sorted(self.valid_coins, reverse=True):
            coin_change[coin] = change // coin
            change %= coin

        user.deposit = 0
        user.save()

        logger.info(f"{user.username} bought {product.product_name}, change: {coin_change}")
        return total_cost,coin_change,product.product_name

