from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

import logging

from .models import User, Product
from .serializers import (
    UserSerializer,
    ProductSerializer,
    DepositInputSerializer,
    DepositOutputSerializer,
    ResetOutputSerializer,
    BuyInputSerializer,
    BuyOutputSerializer
)
from auth_app.permissions import IsSellerOwnerOrReadOnly,IsBuyerPermission
from .services import CoreService

logger = logging.getLogger(__name__)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return super().get_permissions()

    @action(detail=False, methods=['post'], permission_classes=[IsBuyerPermission])
    def deposit(self, request):
        serializer = DepositInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)


        try:
            deposit = CoreService().handle_deposit(request.user, serializer.validated_data['amount'])
        except Exception as e:
            logger.error(f"Deposit failed: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        output = DepositOutputSerializer({'deposit':deposit})
        return Response(output.data)

    @action(detail=False, methods=['post'], permission_classes=[IsBuyerPermission])
    def reset(self, request):

        try:
            deposit = CoreService.handle_reset(request.user)
        except Exception as e:
            logger.error(f"Reset failed: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        output = ResetOutputSerializer({'deposit':deposit})
        return Response(output.data)

    @action(detail=False, methods=['post'], permission_classes=[IsBuyerPermission])
    def buy(self, request):
        serializer = BuyInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            total_cost, coin_change, product_name = CoreService().handle_buy(
                request.user,
                serializer.validated_data['product_id'],
                serializer.validated_data['quantity']
            )
        except Exception as e:
            logger.error(f"Buy failed: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        output = BuyOutputSerializer({'total_spent':total_cost,'product':product_name,'change':coin_change})
        return Response(output.data)
    
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsSellerOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)
