from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /collector/
    url(r'^$', views.index, name='index'),

    # ex: /collector/Diario_Oficial_Uniao/20170201/47
    # Returns a JSON with the text of a particular document inside a DO.
    url(r'^(?P<document_id>\w+/[0-9]+/[0-9]+)/$', views.document, name='document'),

    # ex: /collector/Diario_Oficial_Uniao/20170201
    # Returns a JSON file with a list of links for the pages of the DO.
    url(r'^(?P<journal_id>\w+)/(?P<date>[0-9]+)$', views.journal_by_edition, name='journal by edition'),
]
