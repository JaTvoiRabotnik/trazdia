from pydoc import locate
import logging
import json
from django.http import Http404
from django.http import HttpResponse

logger = logging.getLogger(__name__)


def get_journal_id(first_level, second_level, third_level):
    with open('collector/journal_id.json') as data_file:
        edition_dict = json.load(data_file)
        if(first_level):
            if(second_level):
                if(third_level):
                    return edition_dict[first_level][second_level][third_level]
                else:
                    return edition_dict[first_level][second_level]
            else:
                edition_dict[first_level]
        else:
            return None


def get_from_cache():
    pass


# Request index from the source
def get_index(first_level, second_level, third_level, date):
    journal_id = get_journal_id(first_level, second_level, third_level)
    journal_class = locate('collector.journal.' + journal_id)
    journal = journal_class(date)
    content = journal.return_index()
    if not content:
        raise Http404('Page not found')
    response = HttpResponse(content_type='application/json')
    response.write(content)
    return response


# Try to find document on the cache, otherwise fire worker to get it from the source
def get_full_do(first_level, second_level, third_level, date):
    journal_id = get_journal_id(first_level, second_level, third_level)
    journal_class = locate('collector.journal.' + journal_id)
    journal = journal_class(date)
    content = journal.bring_edition()
    if not content:
        raise Http404('Page not found')
    response = HttpResponse(content_type='application/json')
    response.write(content)
    return response


# Try to find document on the cache, otherwise fire worker to get it from the source
def get_individual_doc(first_level, second_level, third_level, date, document_id):
    pass
