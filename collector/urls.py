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
    url(r'^(?P<journal_id>\w+)/(?P<date>[0-9]+)/(?P<section>\w+)$', views.journal_by_date_and_section, name='journal by date_and_section'),

    # ex: /collector/br/rj/municipio/20160127
    # Returns a JSON file with a list of links for the pages of the DO.
    url(r'^br/(?P<first_level>\w+)/(?P<second_level>\w+)/(?P<date>[0-9]+)$', views.journal_by_date, name='journal by date'),
]
