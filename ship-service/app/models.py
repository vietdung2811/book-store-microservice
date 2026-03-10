from django.db import models

class Shipment(models.Model):
    order_id = models.IntegerField()
    customer_id = models.IntegerField()
    tracking_number = models.CharField(max_length=100, blank=True)
    shipped_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Shipped')

    def __str__(self):
        return f"Shipment for Order {self.order_id}"
