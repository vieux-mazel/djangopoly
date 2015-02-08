from django.db import models

class Effect(models.Model):
	type = models.CharField(max_length=128, unique=True)
	param = models.IntegerField(default=0)