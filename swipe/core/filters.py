from django_filters import FilterSet

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
            'attendence_date': ['contains','range'],
            'work_time': ['contains'],
            'employee_name': ['contains'],
            'employee_dept': ['contains'],
            'tower': ['contains'],
        }
