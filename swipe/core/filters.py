from django_filters import FilterSet, DateRangeFilter
from django.db import models
import django_filters
from .models import Document, Employee

class DocumentFilter(FilterSet):
    class Meta:
        model = Document
        fields = {
            'file_title': ['exact', 'contains'],
            'file_from': ['range']
        }

class EmployeeFilter(FilterSet):
    class Meta:
        model = Employee
        fields = {
            'employee_id': ['exact'],
            'attendence_date': ['range', 'contains'],
            'work_time': ['contains'],
            'employee_name': ['contains'],
            'dept': ['contains'],
            'tower': ['contains'],
        }
    @classmethod
    def filter_for_lookup(cls, f, lookup_type):
        if isinstance(f, models.DateField) and lookup_type == 'range':
            return DateRangeFilter, {}
        return super().filter_for_lookup(f, lookup_type)
