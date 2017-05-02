from django.shortcuts import render
from django.http import HttpResponse
from pydoc import locate
import logging

logger = logging.getLogger(__name__)


def index(request):
    return HttpResponse("TrazDia: colletor de Diarios Oficials")


def document(request, document_id):
    response = "Voce esta vendo a materia %s."
    return HttpResponse(response % document_id)


def journal_by_date_and_section(request, journal_id, date, section):
    journal_class = locate('collector.journal.' + journal_id)
    journal = journal_class(date)
    content = journal.return_index(section)
    response = HttpResponse(content_type='application/json')
    response.write(content)
    return response
