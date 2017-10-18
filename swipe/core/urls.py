from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^upload', views.upload, name='upload'),
    url(r'^mail', views.mail, name='mail'),
    url(r'^test', views.test, name='test'),
    url(r'^table', views.table, name='table'),
    url(r'^analys', views.FilteredDocument.as_view(), name='analys'),

]
