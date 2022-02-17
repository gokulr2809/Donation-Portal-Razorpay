from django.db import models


class donate (models.Model):
    name = models.CharField(max_length=40)
    amount = models.CharField(max_length=20)
    payment_id = models.CharField(max_length=40)
    status = models.BooleanField(default=False)