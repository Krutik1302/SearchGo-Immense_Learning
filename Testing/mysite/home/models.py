from os import link
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import AbstractUser

class MyUser(AbstractUser):
    
    GENDER = [
        ("Male", "Male"),
        ("Female", "Female"),
    ]
    gender = models.CharField(
        choices= GENDER, default="NONE", blank=True, null=True, max_length=30
    )

    contact = models.CharField(
        max_length=11
    )

class Fields(models.Model):
    Field_Name = models.CharField(max_length=60)
    Flag = models.IntegerField(max_length=2, default=0)
    Count = models.IntegerField(max_length=8, default=0)

class Category(models.Model):
    FieldFK = models.ForeignKey(Fields, on_delete=models.CASCADE)
    Category_Name = models.CharField(max_length=60, blank = True)
    Flag = models.IntegerField(max_length=2, default = 0)
    Count = models.IntegerField(max_length=6, default = 0)

class Sub_Category(models.Model):
    CategoryFK = models.ForeignKey(Category, on_delete=models.CASCADE)
    Sub_Name = models.CharField(max_length=60, blank = True)
    Flag = models.IntegerField(max_length=2, default = 0)
    Count = models.IntegerField(max_length=6, default = 0)

class Link(models.Model):
    Sub_CategoryFK = models.ForeignKey(Sub_Category, on_delete=models.CASCADE)
    Data_link = models.URLField(max_length=200, blank=True)
    Count = models.IntegerField(max_length=6, default = 0)
    link_description = models.CharField(max_length=200, blank = True)
    