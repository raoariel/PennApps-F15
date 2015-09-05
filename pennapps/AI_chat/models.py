from django.db import models

class User(models.Model):
    messages = models.BinaryField()
    email = models.EmailField()
    first_name = models.CharField(max_length= 254)
    last_name = models.CharField(max_length= 254)
