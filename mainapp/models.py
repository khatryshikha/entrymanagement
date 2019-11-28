from __future__ import unicode_literals

from datetime import datetime

from django.db import models
from phone_field import PhoneField


class Host(models.Model):
    id = models.CharField(max_length=30, primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    Email_ID = models.EmailField(max_length=70, null=False, blank=False)
    Phone_No = models.IntegerField()


class Visitor(models.Model):
    id = models.CharField(max_length=30, primary_key=True)
    host_id = models.ForeignKey(
        'Host', on_delete=models.PROTECT, null=True)
    first_name = models.CharField(max_length=10)
    last_name = models.CharField(max_length=10)
    Email_ID = models.EmailField(
        max_length=70, null=False, blank=False)
    Phone_No = models.IntegerField()
    Check_in = models.DateTimeField(default=datetime.now, blank=True)
    Check_out = models.DateTimeField(null=True, blank=True)
