from django.db import models

# Create your models here.
class DefaultNetworkSettings(models.Model):
    setting_type_id = models.CharField(max_length=20,default="default")
    default_subnet_name = models.CharField(max_length=24,blank=True)
    default_address_range = models.CharField(max_length=100,blank=True)
    default_address_space = models.CharField(max_length=100,blank=True) 