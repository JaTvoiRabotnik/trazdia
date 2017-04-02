# Collect data from a given source #
# TODO: Make this file more generic #

# -*- coding: utf-8 -*-

# importing modules
import requests
import csv
import io
import sys, getopt


def main(argv):

    # Default parameters
    ediParam = 0
    store = False

    try:
        opts, args = getopt.getopt(argv, "he:s", ["help", "edition=", "store"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-e", "--edition"):
            ediParam = arg
        elif opt in ("-o", "--store"):
            store = True
    if not opts:
        usage()
        sys.exit(2)

    return ediParam, output


def usage():
    print("usage: getHtm [--help] [--edition=<value>]")

# Decode an input and return utf-8 #
def read_hostile_text(encoded_text):
    encodings = [
        'latin_1',
        'utf_16',
        'cp1250',
        'iso-8859-1',
    ]
    for encoding in encodings:
        try:
            decoded_text = encoded_text.decode(encoding)
            return decoded_text.encode('utf-8')
        except UnicodeDecodeError:
            print(encoding, 'did not work. Trying another encoding for', encoded_text)
    print('Could not decode', encoded_text)
    return None

def getedition(ediParam, store):
    # Keep a dictionary of folders and documents
    folders     = []
    materias    = []

    # http response
    response    = requests.get(HTMPARAM.format(ediParam))
    respList    = response.content.split('\n')
    #respList    = open('3168_response.txt')

    for row in respList:
        # Index of a folder
        if 'gFld(' in row:
            fldKey      = row[0:row.find(' = ')]
            fldVal      = read_hostile_text(row[row.find('gFld(')+5:row.find(');')] \
                          .split(', ')[0][1:-1])
            folders.append(dict(fldKey=fldKey, fldVal=fldVal))
        # Index of a document
        elif 'addChild(' in row:
            materia     = row[row.find('([')+2:row.find('])')].split('", "')
            matId       = materia[1][materia[1].find('?id=')+4: \
                          materia[1].find('&edi')]
            # TODO CAREFUL: we might have a hidden comma here, which will cause havoc on the conversion to CSV
            matTitulo   = read_hostile_text(materia[0][1:])
            matPaiKey   = row[0:row.find('.addChild')]
            materias.append(dict(matPathKey=[matPaiKey],
                                 matPathVal='',
                                 matTitulo=matTitulo,
                                 matId=matId,
                                 matEdi=ediParam,
                                 matLink=LNKPARAM.format(matId,ediParam)))
        elif 'addChildren(' in row:
            paiKey      = row[0:row.find('.addChildren')]
            childVals   = row[row.find('([')+2:row.find('])')].split(',')
            for val in childVals:
                for materia in materias:
                    if materia['matPathKey'][0] == val:
                        materia['matPathKey'].insert(0, paiKey)

    for materia in materias:
        for n,i in enumerate(materia['matPathKey']):
            for keyVal in folders:
                if keyVal['fldKey'] == i:
                    materia['matPathVal'] += keyVal['fldVal']
                    if n < len(materia['matPathKey']) - 1:
                        materia['matPathVal'] += ' | '

    # TODO I am not happy with this. We shouldn't be hardcoding the location of the output CSVs
    # Actually, we shouldn't even be outputting them to files here. We should instead output the
    # list of materias, and defer the job of writing the files to a caller.
    if store:
        with open('../data/do-info/' + str(ediParam) + '.csv', 'wb') as csvfile:
            fieldnames = ['matEdi','matId','matPathVal','matTitulo','matLink']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for materia in materias:
                del materia['matPathKey']
                writer.writerow(materia)
    return materias

if __name__ == "__main__":
    ediParam, store = main(sys.argv[1:])
    for materia in getedition(ediParam, store):
        print(materia['matEdi'], materia['matId'], materia['matPathVal'], materia['matTitulo'], materia['matLink'])
