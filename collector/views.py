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

def journal_by_edition(request, journal_id, edition_id):
    journal_class = locate('collector.journal.' + journal_id)
    journal = journal_class(edition_id)
    content = journal.executar()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="diario.pdf"'
    response.write(content)
    return response
