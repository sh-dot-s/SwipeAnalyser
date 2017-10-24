from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from swipe.core.models import Document, Employee, Review
from .tables import BootstrapTable, DocumentTable, EmployeeTable
from django_tables2 import RequestConfig
from django_filters.views import FilterView
from django_tables2 import MultiTableMixin, RequestConfig, SingleTableView
from django_tables2.export.views import ExportMixin
from .filters import DocumentFilter, EmployeeFilter
from .corelogic import *
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from .mail import sendSMTPMail
from django.http import HttpResponse

def home(request):
    documents = Document.objects.all()

    return render(request, 'home.html', {
        'documents': documents
    })

def upload(request):
    if request.method == 'POST' and request.FILES['input-b7[]']:
        fileXL = request.FILES['input-b7[]']
        try:
            if fileXL.name in [documents.file_title for documents in Document.objects.all()]:
                return render(request, 'upload.html', {'alreadyExist': True})
        except Exception as e:
            print(e)
            return render(request, 'upload.html', {'uploadFailed': True})
        else:
            fs = FileSystemStorage()
            filename = fs.save(fileXL.name, fileXL)
            uploaded_file_url = str(fs.url(filename))
            doc = Document(upload_url = uploaded_file_url, file_title = fileXL.name)#, file_from=request.POST["from"], file_to=request.POST["to"]
            doc.save()

            documents = Document.objects.all()
            return render(request, 'upload.html', {'save': True})
    return render(request, 'upload.html')

class FilteredDocument(FilterView, SingleTableView):
    print("Rendering class based view")
    table_class = EmployeeTable
    model = Employee
    template_name = 'filter.html'
    filterset_class = EmployeeFilter
    table_pagination = {'per_page': 50}

def analys(request):
    table = BootstrapTable(Employee.objects.all()) #order_by='-employee_id'
    RequestConfig(request, paginate={'per_page': 50}).configure(table)
    # print(RequestConfig)
    for objs in request:
        print(request)
    return render(request, 'analyse.html',{'documents': table})

@transaction.atomic
@csrf_exempt
def test(request):
    if request.method == 'GET':
        return render(request, 'test.html')
    else:
        for processFile in Document.objects.all():
        # processFile = Document.objects.all()[len(list(Document.objects.all()))-1]
            if not processFile.processed:
                masterEmployee = load_master_emp(processFile.file_title)
                shiftDict,employeeShift,irregularShifts = shift_emp_masters()
                # print(shiftDict,employeeShift,irregularShifts)
                masterList, d1, d2 = calc_time(masterEmployee,employeeShift,irregularShifts,shiftDict,processFile.file_title)
                # delta = processFile.file_to - processFile.file_from
                print(d2, d1)
                delta = d2 - d1
                datesRange = []
                for i in range(delta.days + 1):
                    d = str(d1 + datetime.timedelta(days=i))
                    datesRange.append(d)
                # if not processFile.processed:
                for rows in masterList:
                    # print(rows)
                    work = rows[4:]
                    # print(work)
                    for work,dates in zip(work,datesRange):
                        q = Employee(employee_id=rows[3],attendence_date=dates,work_time=work,employee_name=rows[2],employee_dept=rows[1],tower=rows[0])
                        q.save()
                processFile.processed = True
                processFile.save(update_fields=["processed"])
        return render(request, 'test.html')


def table(request):
    return render(request, 'email.html')

def mail(request):
    table =  Employee.objects.all()
    if request.method == "POST":
        pks = request.POST.getlist("empid")
        selected_objects = Employee.objects.filter(pk__in=pks)
        table = BootstrapTable(selected_objects) #order_by='-employee_id'
        RequestConfig(request, paginate={'per_page': 10}).configure(table)
        sendSMTPMail(selected_objects)
    return render(request, 'selection.html',{'table': table})

@csrf_exempt
def mail_response(request):
    if request.method == 'POST':
        print(request.POST)
        doc = Review(response = request.POST['clarify'], employee_id = '', attendence_date='')#, file_from=request.POST["from"], file_to=request.POST["to"]
        doc.save()
        return HttpResponse("<h4>Response recorded, Thank you for your time.</h4>")
    return HttpResponse("<h3>Invalid Session</h3>")
