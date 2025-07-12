from rest_framework import serializers
from .models import Product
from auth_app.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'role', 'deposit']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            role=validated_data['role']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class ProductSerializer(serializers.ModelSerializer):
    sellerId = serializers.ReadOnlyField(source='seller.id')
    class Meta:
        model = Product
        fields = ['id','product_name', 'cost', 'amount_available', 'sellerId']

        def validate_cost(self, value):
            if value % 5 != 0:
                raise serializers.ValidationError("Cost must be divisible by 5.")
            return value



class DepositInputSerializer(serializers.Serializer):
    amount = serializers.IntegerField()

    def validate_amount(self, value):
        if value % 5 != 0:
            raise serializers.ValidationError("Deposit amount must be divisible by 5.")
        return value


class DepositOutputSerializer(serializers.Serializer):
    deposit = serializers.IntegerField()


class ResetOutputSerializer(serializers.Serializer):
    deposit = serializers.IntegerField()


class BuyInputSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1, default=1)

class BuyOutputSerializer(serializers.Serializer):
    total_spent = serializers.IntegerField()
    product = serializers.CharField()
    change = serializers.DictField(child=serializers.IntegerField())


