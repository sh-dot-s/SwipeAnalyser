from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^upload$', views.upload, name='upload'),
    url(r'^uploadMaster', views.uploadMaster, name='uploadMaster'),
    url(r'^mail$', views.mail, name='mail'),
    url(r'^test', views.test, name='test'),
    url(r'^create', views.create, name='create'),
    url(r'^deleteFiles', views.deleteFiles, name='deleteFiles'),
    url(r'^table', views.table, name='table'),
    url(r'^quote', views.getQuote, name='quote'),
    url(r'^getEmpDetails/(?P<item_pk>\w+&[\d+-]+)', views.details, name='details'),
    url(r'^ifDatePresent/(?P<item_pk>\w+&[\d+-]+)', views.ifDetailsPresent, name='ifDetailsPresent'),
    url(r'^getDocDetails/(?P<graph_id>[A-Za-z\s\._0-9,\w+]+)', views.getDocDetails, name='getDocDetails'),
    url(r'^mail_response/$', views.mail_response, name='mail_response'),
    url(r'^analys', views.FilteredDocument.as_view(), name='analys'),

]
