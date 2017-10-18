from __future__ import unicode_literals
from datetime import datetime
from django.db import models

class Document(models.Model):
    upload_url = models.CharField(max_length=255, blank=True)
    file_title = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateField(auto_now_add=True)
    file_from = models.DateField(default=datetime(1990,1,1),blank=True)
    file_to = models.DateField(default=datetime(1990,1,1),blank=True)
    processed = models.BooleanField(default=False)
    def __unicode__(self):
        return self.file_title

    def get_absolute_url(self):
        return '/%d' % self.upload_url

class Employee(models.Model):
    employee_id = models.CharField(max_length=255, blank=True)
    attendence_date = models.DateField(default=None,blank=True)
    work_time = models.CharField(max_length=255, blank=True)
    employee_name = models.CharField(max_length=255, blank=True)
    employee_dept = models.CharField(max_length=255, blank=True)
    tower = models.CharField(max_length=255, blank=True)

# class EmployeeMeta(models.Model):
#     jsonData = models.CharField(blank=True)
#     employee_id = models.CharField(max_length=255, blank=True)
#     attendence_date = models.DateField(default=None,blank=True)
