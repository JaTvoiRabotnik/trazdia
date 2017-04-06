from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /collector/
    url(r'^$', views.index, name='index'),
    # ex: /collector/Diario_Oficial_Uniao/20170201/47
    url(r'^(?P<document_id>\w+/[0-9]+/[0-9]+)/$', views.document, name='document'),
    url(r'^(?P<journal_id>\w+)/(?P<edition_id>[0-9]+)$', views.journal_by_edition, name='journal by edition'),
]
