import collector
from collector import getDocument
import sys, getopt

# Test script. Given a metadata file with editions and document IDs, get all documents in it.

def main(argv):

    # Default parameters
    input_location = ''
    output_path = ''

    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["help", "input=", "output="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-i", "--input"):
            input_location = arg
        elif opt in ("-o", "--output"):
            if arg[-1] is not '/':
                output_path = arg + '/'
            else:
                output_path = arg
    if not opts:
        usage()
        sys.exit(2)

    if output_path == '' or input_location == '':
        print("input and output are mandatory parameters.")
        usage()
        sys.exit(2)

    return input_location, output_path


def usage():
    print("usage: collect_htmls [--help] [--input=<path and file>] [--output=<path>]")
    print("--help: prints this usage guide and exits.")
    print("--input=<path and file>: pass in the path and file name of the meta data.")
    print("--output=<path>: pass in the path where outputs are to be stored.")


if __name__ == "__main__":
    input_location, output_path = main(sys.argv[1:])

    metafile = open(input_location, 'r')
    for entry in metafile:
        entry_address = entry.split(',')
        ediParam = entry_address[0]
        matParam = entry_address[1].replace('\n', '')
        link = collector.LNKPARAM.format(ediParam, matParam)
        htmlfile = getDocument.extract_html_from_link(link)
        print('Outputting html to', output_path + str(matParam) + '.html')
        f = open(output_path + str(matParam) + '.html', 'w')
        for line in htmlfile:
            f.write(line)
        f.close()
