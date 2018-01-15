from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from swipe.core.models import Document, Employee, EmployeeComplete
from .tables import BootstrapTable, DocumentTable, EmployeeTable, ModalPopUpTable
from django_tables2 import RequestConfig
from django_filters.views import FilterView
from django_tables2 import MultiTableMixin, RequestConfig, SingleTableView
from django_tables2.export.views import ExportMixin
from .filters import DocumentFilter, EmployeeFilter
from .corelogic import *
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from .mail import sendSMTPMail
from django.http import HttpResponse, JsonResponse
import nested_dict
from django.core import serializers
from django.db.models import Count
from django.db.models import Q
from django.conf import settings
from time import sleep
import threading

quoteFile = open(os.path.join(settings.STATICFILES_DIRS[0],"quotes.json"),'r')
quotes = json.load(quoteFile)

def home(request):
    documents = Document.objects.all()

    return render(request, 'home.html', {
        'documents': documents
    })

@csrf_exempt
def upload(request):
    if request.method == 'POST' and request.FILES['input-b7[]']:
        fileXL = request.FILES['input-b7[]']
        print(fileXL)
        try:
            if fileXL.name in [documents.file_title for documents in Document.objects.all()]:
                return JsonResponse({'error': '%sFile already exists'%fileXL.name})
        except Exception as e:
            print(e)
            return JsonResponse({'error': '%s upload failed'%fileXL.name})
        else:
            fs = FileSystemStorage()
            filename = fs.save(fileXL.name, fileXL)
            uploaded_file_url = str(fs.url(filename))
            doc = Document(upload_url = uploaded_file_url, file_title = fileXL.name)#, file_from=request.POST["from"], file_to=request.POST["to"]
            doc.save()

            documents = Document.objects.all()
            return JsonResponse({})
    return render(request, 'upload.html')

class FilteredDocument(FilterView, SingleTableView):
    table_class = EmployeeTable
    model = Employee
    template_name = 'filter.html'
    filterset_class = EmployeeFilter
    pages = 25
    table_pagination = {'per_page': pages}

def analys(request):
    table = BootstrapTable(Employee.objects.all()) #order_by='-employee_id'
    RequestConfig(request, paginate={'per_page': 50}).configure(table)
    # print(RequestConfig)
    for objs in request:
        print(request)
    return render(request, 'analyse.html',{'documents': table})

@csrf_exempt
def test(request):
    t = threading.Thread(target=start_processing, args=(), kwargs={})
    t.setDaemon(True)
    status = None

    if request.method == 'GET':
        if request.is_ajax():
            if t.isAlive():
                return JsonResponse({'status': 'running'})
            else:
                try:
                    for processFile in Document.objects.all():
                        if not processFile.processed and not status:
                            status = True
                    if not status:
                        return JsonResponse({'status': 'completed'})
                    else:
                        return JsonResponse({'status': 'running'})
                except Exception as e:
                    print(e)
                    return JsonResponse({'status': 'running'})
        else:
            return render(request, 'test.html')
    else:
        t.start()
        return JsonResponse({'status': 'started'})
       
                

@transaction.atomic
def start_processing():
    for processFile in Document.objects.all():
        # processFile = Document.objects.all()[len(list(Document.objects.all()))-1]
            if not processFile.processed:
                masterEmployee, employeeComplete = load_master_emp(processFile.file_title)
                for cell in employeeComplete:
                    dateEmp, timeEmp = cell[0].value,cell[1].value
                    site, card, empid, cid = int(cell[2].value),int(cell[3].value),str(cell[4].value),int(cell[8].value)
                    empname, dept, typ, gate, inout, remark = str(cell[5].value),str(cell[6].value),str(cell[7].value),str(cell[9].value),str(cell[10].value),str(cell[11].value)
                    try:
                        if isinstance(dateEmp, datetime.datetime):
                            formattedDate = dateEmp.date()
                        else:
                            formattedDate = datetime.datetime.strptime(dateEmp, "%d/%m/%Y").date()
                    except:
                        if isinstance(dateEmp, datetime.datetime):
                            formattedDate = dateEmp.date()
                        else:
                            formattedDate = datetime.datetime.strptime(dateEmp, "%d-%m-%Y").date()

                    if isinstance(timeEmp, datetime.datetime):
                        formattedTime = timeEmp.time()
                    else:
                        formattedTime = (datetime.datetime.strptime(timeEmp, "%H:%M:%S")).time()

                    q=EmployeeComplete(dat=formattedDate,tim=formattedTime,sitecode=site,cardid=card,empid=empid,empname=empname,department=dept,typ=typ,cid=cid,gate=gate,inout=inout,remark=remark)
                    q.save()

                shiftDict,employeeShift,irregularShifts = shift_emp_masters()
                # print(shiftDict,employeeShift,irregularShifts)
                timeDict, d1, d2 = calc_time(masterEmployee,employeeShift,irregularShifts,shiftDict,processFile.file_title)
                # delta = processFile.file_to - processFile.file_from
                # print(d2, d1)
                delta = d2 - d1
                datesRange = []
                for i in range(delta.days + 1):
                    d = str(d1 + datetime.timedelta(days=i))
                    datesRange.append(d)
                # if not processFile.processed:
                for keys in timeDict.keys():
                    for dates in datesRange:
                        if not Employee.objects.filter(employee_id=keys,attendence_date=dates).exists():
                            q = Employee(employee_id=keys,attendence_date=dates,work_time="NS",employee_name=employeeShift[keys][2],dept=employeeShift[keys][1],tower=employeeShift[keys][0])
                            q.save()
                for keys,value in timeDict.items_flat():
                    if Employee.objects.filter(employee_id=keys[0],attendence_date=keys[1]).exists():
                        empObj = Employee.objects.filter(employee_id=keys[0],attendence_date=keys[1]).update(work_time=value)
                processFile.file_from = datesRange[0]
                processFile.file_to = datesRange[-1]
                processFile.processed = True
                processFile.records = len(employeeComplete)
                processFile.save(update_fields=["processed","file_to","file_from",'records'])  
                print("process complete")
    return

def table(request):
    return render(request, 'email.html')

@csrf_exempt
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
        for keys in request.POST:
            response = (request.POST.getlist(keys))
            details = keys.split("_")
            date = datetime.datetime.strptime(details[2],"%Y-%m-%d").date()
            response = response[0]
            Employee.objects.filter(employee_id=details[1], attendence_date=date).update(emp_response = response)
             # Review(response = response, employee_id = details[1], attendence_date=date)#, file_from=request.POST["from"], file_to=request.POST["to"]
        return HttpResponse("<h4>Response recorded, Thank you for your time.</h4>")
    return HttpResponse("<h3>Invalid Session</h3>")

def details(request, item_pk):
    item_pk = item_pk.split("&")
    # print(item_pk)
    date = datetime.datetime.strptime(item_pk[1], "%Y-%m-%d").date()
    table = EmployeeComplete.objects.filter(
        empid=item_pk[0],
        dat__year=date.year,
        dat__month=date.month,
        dat__day=date.day
    )
    response = serializers.serialize('json', table)
    return HttpResponse(response, content_type='application/json')

def getDocDetails(request, graph_id):
    print(graph_id)
    docDetails = Document.objects.get(file_title=graph_id.split("_")[1])
    start = docDetails.file_from
    end = docDetails.file_to
    delta = end - start
    dates, count = [], []
    for i in range(delta.days + 1):
        date = (start + datetime.timedelta(days=i))
        dates.append(date)
        temp = Employee.objects.filter(attendence_date = date).exclude(work_time="NS").extra({'date':"attendence_date"}).values('date').annotate(date_count=Count('attendence_date'))
        count.append(temp.values_list('date_count', flat=True)[0])
    data = {
        'count': count,
        'labels': dates
    }
    return JsonResponse(data)

def getQuote(request):
    from random import randint
    quoteNums = randint(15, 25)
    print(quoteNums)
    q,a = [],[]
    for i in range(quoteNums):
        q.append("<p>"+quotes[randint(0,len(quotes))]["quoteText"]+"</p>")
        a.append(quotes[randint(0,len(quotes))]["quoteAuthor"])
    data = {
        "quotes": q,
        "authors": a
    }
    return JsonResponse(data)

@csrf_exempt
def uploadMaster(request):
    if request.method == 'POST' and request.FILES['input-b6[]']:
        fileXL = request.FILES['input-b6[]']
        print(fileXL)
    return JsonResponse({'error':'got the file, jus kidding'})

def alive(request):
    return HttpResponse("Server alive --- to avoid server timeout")
