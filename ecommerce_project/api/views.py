from rest_framework import viewsets
from .models import Order, Customer, Product
from .serializers import CustomerSerializer, ProductSerializer, OrderSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        customer_name = self.request.query_params.get('customer')
        product_names = self.request.query_params.get('products')

        if customer_name:
            queryset = queryset.filter(customer__name__iexact=customer_name)

        if product_names:
            product_names = product_names.split(',')
            queryset = queryset.filter(
                order_items__product__name__in=product_names
            ).distinct()

        return queryset
