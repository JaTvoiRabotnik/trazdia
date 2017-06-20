from django.shortcuts import render
from django.http import HttpResponse
import commander

def index(request):
    return HttpResponse("TrazDia: colletor de Diarios Oficials")


def document(request, document_id):
    response = "Voce esta vendo a materia %s."
    return HttpResponse(response % document_id)



# Receives an index request from urls.py and defers to commander
def command_get_index_3(request, first_level, second_level, third_level, date):
    return commander.get_index(first_level, second_level, third_level, date)

# Receives an index request from urls.py and defers to commander
def command_get_index_2(request, first_level, second_level, date):
    return commander.get_index(first_level, second_level, None, date)

# Receives an index request from urls.py and defers to commander
def command_get_index_1(request, first_level, date):
    return commander.get_index(first_level, None, None, date)



# Receives a full DO request from urls.py and defers to commander
def command_get_full_do_3(request, first_level, second_level, third_level, date):
    return commander.get_full_do(first_level, second_level, third_level, date)

# Receives a full DO request from urls.py and defers to commander
def command_get_full_do_2(request, first_level, second_level, date):
    return commander.get_full_do(first_level, second_level, None, date)

# Receives a full DO request from urls.py and defers to commander
def command_get_full_do_1(request, first_level, date):
    return commander.get_full_do(first_level, None, None, date)



# Receives an individual document request from urls.py and defers to commander
def command_get_individual_doc_3(request, first_level, second_level, third_level, date, document_id):
    return commander.get_individual_doc(first_level, second_level, third_level, date, document_id)

# Receives an individual document request from urls.py and defers to commander
def command_get_individual_doc_2(request, first_level, second_level, date, document_id):
    return commander.get_individual_doc(first_level, second_level, None, date, document_id)

# Receives an individual document request from urls.py and defers to commander
def command_get_individual_doc_1(request, first_level, date, document_id):
    return commander.get_individual_doc(first_level, None, None, date, document_id)



###############################################################################

# Check whether worker has finished what it was doing
def check_worker(request):
    worker_id = request.GET.get('worker_id', None)
    response = "Checking worker with ID %s."
    return HttpResponse(response % worker_id)
