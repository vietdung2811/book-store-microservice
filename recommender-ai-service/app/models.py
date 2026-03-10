from django.db import models

class Recommendation(models.Model):
    customer_id = models.IntegerField()
    recommended_book_id = models.IntegerField()
    score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Recommendation for {self.customer_id}"
