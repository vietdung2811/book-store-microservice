from django.db import models

class Manager(models.Model):
    name = models.CharField(max_length=255)
    department = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.name} - {self.department}"
