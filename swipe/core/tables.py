import django_tables2 as tables
from .models import Document, Employee, EmployeeComplete
from django.contrib.auth.models import User

class BootstrapTable(tables.Table):

    class Meta:
        model = Employee
        attrs = {'class': 'table table-bordered table-striped table-hover'}
        orderable = False

class DocumentTable(tables.Table):

    class Meta:
        model = Document
        attrs = {'class': 'table table-bordered table-striped table-hover'}

class EmployeeTable(tables.Table):
    empid = tables.CheckBoxColumn(verbose_name=('Select'), accessor="pk", orderable=False)
    # customer = tables.LinkColumn('detail', args=[A('pk')])
    # detailsFound = EmployeeComplete.objects.filter(empname = pk.empname)
    view_data = tables.TemplateColumn(
        '''
        <button id = 'modalBtn{{record.employee_id}}{{record.attendence_date|date:"Ymd"}}' type="button" class="btn btn-info btn-sm" data-toggle="modal" value = "{{record.employee_id}}&{{record.attendence_date|date:"Y-m-d"}}" data-target="#myModal">View Details</button>
        '''
        )

    class Meta:
        model = Employee
        attrs = {'id': 'master_table', 'class': 'table table-striped table-hover'}
        sequence = ('empid', 'employee_id','tower','dept','employee_name','attendence_date','day','code','work_time',"emp_response")
        fields = ('empid', 'employee_id','tower','dept','employee_name','attendence_date','day','code','work_time',"emp_response")
        orderable = False

class ModalPopUpTable(tables.Table):

        class Meta:
            model = EmployeeComplete
            attrs = {'class': 'table table-bordered table-striped table-hover'}

class UserTable(tables.Table):
    _ = tables.TemplateColumn(
        '''
        <button id='formbtn-delete' type="button" class="btn btn-sm btn-link" data-toggle="modal" data-target="#deleteconfirm" value="{{record.id}}">Delete</button>&nbsp;&nbsp;
        ''',
        accessor="pk", orderable=False)
    class Meta:
        model = User
        attrs = {'class': 'table table-bordered table-striped table-hover'}
        sequence = ('username', 'first_name', 'last_name', 'email', 'is_active', 'last_login', 'date_joined')
        fields = ('username', 'first_name', 'last_name', 'email', 'is_active', 'last_login', 'date_joined')
