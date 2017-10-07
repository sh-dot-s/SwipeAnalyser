from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^upload', views.upload, name='upload'),
    url(r'^analys', views.analys, name='analys'),
    url(r'^test', views.test, name='test'),
    url(r'^table', views.table, name='table'),
    url(r'^filtered/', views.FilteredDocument.as_view(), name='filtertableview'),

]
