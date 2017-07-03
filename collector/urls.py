from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /collector/
    url(r'^$', views.index, name='index'),

    # ex: /collector/br/rj/rio_de_janeiro/executivo/20160127/index
    # Returns a JSON file with a list of links for the pages of the DO.
    url(r'^br/(?P<first_level>\w+)/(?P<second_level>\w+)/(?P<third_level>\w+)/(?P<date>[0-9]+)/index$', views.command_get_index_3, name='get_index_3'),

    # ex: /collector/br/rj/executivo/20160127/index
    # Returns a JSON file with a list of links for the pages of the DO.
    url(r'^br/(?P<first_level>\w+)/(?P<second_level>\w+)/(?P<date>[0-9]+)/index$', views.command_get_index_2, name='get_index_2'),

    # ex: /collector/br/executivo/20160127/index
    # Returns a JSON file with a list of links for the pages of the DO.
    url(r'^br/(?P<first_level>\w+)/(?P<date>[0-9]+)/index$', views.command_get_index_1, name='get_index_1'),

    # handles polling request for async process
    url(r'^ajax/check_worker/$', views.check_worker, name='check_worker'),

    # hello world for database connection - stored procedures
    url(r'^helloworld$', views.helloworld, name='hello_world'),
]
