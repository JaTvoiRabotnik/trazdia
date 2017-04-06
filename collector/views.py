from django.shortcuts import render
from django.http import HttpResponse
from pydoc import locate

def index(request):
    return HttpResponse("TrazDia: colletor de Diarios Oficials")

def document(request, document_id):
    response = "Voce esta vendo a materia %s."
    return HttpResponse(response % document_id)

def journal_by_edition(request, journal_id, edition_id):
    journal_class = locate('collector.journal.' + journal_id)
    journal = journal_class(edition_id)
    response = journal.executar()
    return HttpResponse(response)
