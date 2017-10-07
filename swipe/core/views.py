from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from swipe.core.models import Document
from .tables import BootstrapTable, DocumentTable
from django_tables2 import RequestConfig
from django_filters.views import FilterView
from django_tables2 import MultiTableMixin, RequestConfig, SingleTableView
from django_tables2.export.views import ExportMixin
from .filters import DocumentFilter

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
            doc = Document(upload_url = uploaded_file_url, file_title = fileXL.name, file_from=request.POST["from"], file_to=request.POST["to"])
            doc.save()

            documents = Document.objects.all()
            return render(request, 'upload.html', {'save': True})
    return render(request, 'upload.html')

class FilteredDocument(FilterView, SingleTableView):
    print("Rendering class based view")
    table_class = DocumentTable
    model = Document
    template_name = 'filter.html'
    filterset_class = DocumentFilter
    table_pagination = {'per_page': 3}

def analys(request):
    table = BootstrapTable(Document.objects.all(), order_by='-file_title')
    RequestConfig(request, paginate={'per_page': 3}).configure(table)
    print(RequestConfig)
    for objs in request:
        print(request)
    return render(request, 'analyse.html',{'documents': table})

def test(request):
    return render(request, 'test.html')
def table(request):
    return render(request, 'django_tables2/table.html')
