from django_filters import FilterSet

from .models import Document


class DocumentFilter(FilterSet):
    class Meta:
        model = Document
        fields = {
            'file_title': ['exact', 'contains'],
            'file_from': ['range']
        }
