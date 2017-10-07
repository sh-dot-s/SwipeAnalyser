import django_tables2 as tables
from .models import Document


class BootstrapTable(tables.Table):

    class Meta:
        model = Document
        template = 'django_tables2/bootstrap.html'
        attrs = {'class': 'table table-bordered table-striped table-hover'}

class DocumentTable(tables.Table):

    class Meta:
        model = Document
        attrs = {'class': 'table table-bordered table-striped table-hover'}
