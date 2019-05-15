from django.db import models

class Subject(models.Model):
    title = models.CharField(max_length=30)
    slug = models.CharField(max_length=30)

class Temperatura(models.Model):
	temperatura = models.CharField(max_length=30)