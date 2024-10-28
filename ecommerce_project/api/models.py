from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=100, unique=True)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name


class Order(models.Model):
    order_number = models.CharField(max_length=10, unique=True, editable=False)
    customer = models.ForeignKey(Customer, related_name="orders", on_delete=models.CASCADE)
    order_date = models.DateField()
    address = models.TextField()

    def save(self, *args, **kwargs):
        if not self.order_number:
            latest_order = Order.objects.all().order_by('id').last()
            order_num = 1 if not latest_order else int(latest_order.order_number[3:]) + 1
            self.order_number = f'ORD{order_num:05}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.order_number} - {self.customer.name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.order} - {self.product.name} ({self.quantity})"
