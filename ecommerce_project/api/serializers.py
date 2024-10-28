from rest_framework import serializers
from .models import Customer, Product, Order, OrderItem
from datetime import date


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def validate_weight(self, value):
        if value <= 0 or value > 25:
            raise serializers.ValidationError("Weight must be positive and no more than 25kg.")
        return value


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'order_number', 'customer', 'order_date', 'address', 'order_items']

    def validate(self, data):
        total_weight = sum(
            item['product'].weight * item['quantity']
            for item in data.get('order_items')
        )
        if total_weight > 150:
            raise serializers.ValidationError({"total_weight": "Total order weight cannot exceed 150kg."})
        if data.get('order_date') < date.today():
            raise serializers.ValidationError({"order_date": "Order date cannot be in the past."})
        return data

    def create(self, validated_data):
        order_items_data = validated_data.pop('order_items')
        order = Order.objects.create(**validated_data)

        for item_data in order_items_data:
            OrderItem.objects.create(order=order, **item_data)

        return order

    def update(self, instance, validated_data):
        instance.customer = validated_data.get('customer', instance.customer)
        instance.order_date = validated_data.get('order_date', instance.order_date)
        instance.address = validated_data.get('address', instance.address)
        instance.save()

        order_items_data = validated_data.pop('order_items', [])

        for item_data in order_items_data:
            product = item_data.get('product')
            quantity = item_data.get('quantity')

            OrderItem.objects.update_or_create(
                order=instance,
                product=product,
                defaults={'quantity': quantity}
            )

        return instance

