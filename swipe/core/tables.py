import django_tables2 as tables
from .models import Document, Employee, EmployeeComplete


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
    # customer = tables.LinkColumn('detail', args=[A('pk')])
    # detailsFound = EmployeeComplete.objects.filter(empname = pk.empname)
    view_data = tables.TemplateColumn(
        '''
        <button id = 'modalBtn{{record.employee_id}}{{record.attendence_date|date:"Ymd"}}' type="button" class="btn btn-info btn-sm" data-toggle="modal" value = "{{record.employee_id}}&{{record.attendence_date|date:"Y-m-d"}}" data-target="#myModal">View Details</button>
        '''
        )

    class Meta:
        model = Employee
        attrs = {'class': 'table table-bordered table-striped table-inverse table-hover'}
        sequence = ('empid', 'employee_id','tower','dept','employee_name','attendence_date','work_time',"emp_response")
        fields = ('empid', 'employee_id','tower','dept','employee_name','attendence_date','work_time',"emp_response")

class ModalPopUpTable(tables.Table):

        class Meta:
            model = EmployeeComplete
            attrs = {'class': 'table table-bordered table-striped table-hover'}
