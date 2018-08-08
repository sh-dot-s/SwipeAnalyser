from __future__ import unicode_literals
from datetime import datetime
from django.db import models

class Document(models.Model):
    upload_url = models.CharField(max_length=255, blank=True)
    file_title = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_from = models.DateField(default=datetime(1990,1,1),blank=True)
    file_to = models.DateField(default=datetime(1990,1,1),blank=True)
    processed = models.BooleanField(default=False)
    records = models.CharField(max_length=255, blank=True)
    def __str__(self):
        return self.file_title

    def get_absolute_url(self):
        return '/{}'.format(self.upload_url)

class Employee(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, default=None)
    employee_id = models.CharField(max_length=255, blank=True)
    attendence_date = models.DateField(default=None,blank=True)
    day = models.CharField(max_length=255, blank=True)
    code = models.CharField(max_length=1, blank=True)
    work_time = models.CharField(max_length=255, blank=True)
    employee_name = models.CharField(max_length=255, blank=True)
    dept = models.CharField(max_length=255, blank=True)
    tower = models.CharField(max_length=255, blank=True)
    emp_response = models.CharField(max_length=255, blank=False, default="No Response")
    def __str__(self):
        return '{}_{}_{}'.format(self.employee_id,self.employee_name, self.attendence_date)

class EmployeeComplete(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, default=None)
    dat = models.DateField(blank=True)
    tim = models.TimeField(blank = True)
    sitecode = models.IntegerField(blank=True)
    cardid = models.IntegerField(blank=True)
    empid = models.CharField(max_length=255, blank=True)
    empname	= models.CharField(max_length=255, blank=True)
    department = models.CharField(max_length=255, blank=True)
    typ = models.CharField(max_length=255, blank=True)
    cid	= models.IntegerField(blank=True)
    gate = models.CharField(max_length=255, blank=True)
    inout = models.CharField(max_length=255, blank=True)
    remark = models.CharField(max_length=255, blank=True)
    def __str__(self):
        return '{}_{}_{}'.format(self.empid,self.empname, self.dat)
    