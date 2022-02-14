from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Store(models.Model):
     name = models.CharField(max_length=50)
     postcode=models.CharField(max_length=50)
     contact_infor=models.CharField(max_length=50)
     offer_delivery=models.BooleanField(default=True)

class Product(models.Model):
  name = models.CharField(max_length=100)
  category = models.CharField(max_length=100)
  description = models.TextField(max_length=250)
  stores = models.ManyToManyField(Store)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return reverse('detail', kwargs={'product_id': self.id})

class Photo(models.Model):
    url=models.CharField(max_length=200)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    def __str__(self):
        return f"Photo for product_id: {self.product_id} @{self.url}"
