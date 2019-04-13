from django.db import models


class SpisokSM(models.Model):
    access_token = models.CharField(max_length=100, null=True)
    user_id = models.CharField(max_length=100, null=True)

