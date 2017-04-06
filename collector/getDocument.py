# -*- coding: utf-8 -*-

# importing modules
import requests
import csv
from bs4 import BeautifulSoup
import pkg_resources
import unicodedata
import sys, getopt
import json


def main(argv):

    # Default parameters
    ediParam = 0
    matParam = 0
    output = False
    path = ''
    output_format = ''

    try:
        opts, args = getopt.getopt(argv, "he:d:s:o:", ["help", "edition=", "document=", "store=", "output="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-e", "--edition"):
            ediParam = arg
        elif opt in ("-d", "--document"):
            matParam = arg
        elif opt in ("-s", "--store"):
            output = True
            if arg[-1] is not '/':
                path = arg + '/'
            else:
                path = arg
        elif opt in ("-o", "--output"):
            output_format = arg
            if output_format not in ["html", "HTML", "json", "JSON"]:
                print("Invalid output format!")
                usage()
                sys.exit()
    if not opts:
        usage()
        sys.exit(2)

    if ediParam == 0 or matParam == 0 or output_format == '':
        print("edition, document and output are mandatory parameters.")
        usage()
        sys.exit(2)

    return ediParam, matParam, output, path, output_format.lower()


def usage():
    print("usage: getMateria [--help] [--edition=<value>] [--document=<value>] [--store=<path>] [--output=<html/json>]")
    print("--help: prints this usage guide and exits")
    print("--edition=<value>: pass in the edition number to extract")
    print("--document=<value>: pass in the document ID to extract.")
    print("--store=<path>: optional parameter to pass in the path where document is to be extracted to.")
    print("--output=<html/json>: required output, HTML or structured JSON.")


def soupify(link):
    # http response
    response    = requests.get(link)
    #rawtext     = response.content.replace('\n', ' ').replace('\r', '')
    rawtext     = response.content
    soup        = BeautifulSoup(rawtext, 'html5lib')
    return soup

def extract_json(materia):
    soup = soupify(materia['matLink'])
    # This becomes necessary because the raw html is too dirty (more than one head, for example)
    # and ends up confusing the parser.
    soup.head.extract()
    if soup.style is None:
        print(soup.get_text())
        sys.exit()
    else:
        soup.style.extract()
        soup.style.extract()

    enriched_output = [materia['matPathVal'], materia['matTitulo']]
    document = soup.get_text()
    output = materia['matPathVal'] + " " + materia['matTitulo'] + " " + document.encode('utf-8')
    return output

# TODO get the tokens. Right now just outputting a list of strings.
def extract_tokens(materia):
    soup = soupify(materia['matLink'])
    # This becomes necessary because the raw html is too dirty (more than one head, for example)
    # and ends up confusing the parser.
    soup.head.extract()
    if soup.style is None:
        print(soup.get_text())
        sys.exit()
    else:
        soup.style.extract()
        soup.style.extract()

    # This contains the text of the document separated by sentences.
    # Bear in mind that due to ugly and automated formatting when the text was originally generated
    # there might be odd splits, like one word showing up as two separate strings. This will need to
    # be taken care of when structuring the data.
    document = soup.get_text().replace(u'\u00A0', ' ')
    document = document.replace(u'\u000A', '')
    document = document.replace(u'\u0009', '')
    encoded_document = document.encode('utf-8')
    matPathVal = materia['matPathVal']
    matTitulo = materia['matTitulo']
    output = matPathVal + " " + matTitulo + " " + encoded_document
    return output

def extract_html(materia):
    soup = soupify(materia['matLink'])
    return soup.prettify().encode('utf-8')

def extract_html_from_link(link):
    soup = soupify(link)
    return soup.prettify()


if __name__ == "__main__":
    ediParam, matParam, store, path, output = main(sys.argv[1:])

    materias = getMetadata.getedition(ediParam, False)
    for materia in materias:
        if matParam == materia['matId']:
            if output == 'json':
                jsonfile = extract_tokens(materia)
                if not store:
                    print(jsonfile)
                else:
                    print('Outputting json to', path, str(ediParam) + '-' + str(matParam) + '.json')
                    f = open(path + str(ediParam) + '-' + str(matParam) + '.json', 'w')
                    for line in jsonfile:
                        f.write(line)
                    f.close()
                break
                break
            elif output == 'html':
                htmlfile = extract_html(materia)
                if not store:
                    print(htmlfile)
                else:
                    print('Outputting html to', path, str(ediParam) + '-' + str(matParam) + '.html')
                    f = open(path + str(ediParam) + '-' + str(matParam) + '.html', 'w')
                    for line in htmlfile:
                        f.write(line)
                    f.close()
                break
