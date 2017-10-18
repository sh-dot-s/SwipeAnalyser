import django_tables2 as tables
from .models import Document, Employee#, EmployeeMeta


class BootstrapTable(tables.Table):

    class Meta:
        model = Employee
        template = 'django_tables2/bootstrap.html'
        attrs = {'class': 'table table-bordered table-striped table-hover'}

class DocumentTable(tables.Table):

    class Meta:
        model = Document
        attrs = {'class': 'table table-bordered table-striped table-hover'}

class EmployeeTable(tables.Table):
    empid = tables.CheckBoxColumn(verbose_name=('Select'), accessor="pk", orderable=False)

    class Meta:
        model = Employee
        attrs = {'class': 'table table-bordered table-striped table-inverse table-hover'}
        sequence = ('empid', 'employee_id','tower','employee_name','employee_dept','attendence_date','work_time')
        fields = ('empid', 'employee_id','tower','employee_name','employee_dept','attendence_date','work_time')

# class EmployeeRecordsJsonTable(tables.Table):
#     jsonField = tables.JSONColumn()
#     class Meta:
#         model = EmployeeMeta
