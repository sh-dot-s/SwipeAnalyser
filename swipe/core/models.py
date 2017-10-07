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
