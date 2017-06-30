from pydoc import locate
import logging
import json
from django.http import Http404
from django.http import HttpResponse
import psycopg2
from config import config

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


def hello_world():
    ### Connect to the PostgreSQL database server ###
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

 # execute a statement
        cur.callproc('issn.n2c', (115))

        # display the PostgreSQL database server version
        function_return= cur.fetchone()
        response = HttpResponse(content_type='text/html')
        response.write(function_return)

     # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            return response
