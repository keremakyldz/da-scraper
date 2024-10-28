from django.db import models

# Create your models here.
class Brands(models.Model):
    brand_name = models.CharField(max_length=50)
    model_name = models.CharField(max_length=150)
    price_tag = models.CharField(max_length=10 ,default="Unknown-?€")

    def __str__(self):
        return self.brand_name