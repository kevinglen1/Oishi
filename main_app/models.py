from django.db import models
from django.urls import reverse
from datetime import date
# Import the User
from django.contrib.auth.models import User

# class Product(models.Model):

#   stores = models.ManyToManyField(Store)
#   # Add the foreign key linking to a user instance
#   user = models.ForeignKey(User, on_delete=models.CASCADE)