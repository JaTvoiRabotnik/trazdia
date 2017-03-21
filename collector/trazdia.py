#!/usr/bin/env python
# -*- coding: utf8 -*-

#-----------------------------------------------------------------------------
# Copyright 2009 Andrés Mantecon Ribeiro Martano
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>
#-----------------------------------------------------------------------------

import sys
import getopt
import subprocess
from subprocess import Popen
import os
import datetime
import pickle
from threading import Thread
import time
from pydoc import locate

from journal import Journal


def main(argv):

    # Default parameters
    call_function = ""
    journal = ""
    edition = ""

    try:
        opts, args = getopt.getopt(argv, "hc:j:e:", ["help", "call=", "journal=", "edition="])
    except getopt.GetoptError:
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            sys.exit()
        elif opt in ("-c", "--call"):
            call_function = arg
        elif opt in ("-j", "--journal"):
            journal = arg
        elif opt in ("-e", "--edition"):
            edition = arg

    if not opts:
        sys.exit(2)

    if call_function == "":
        print("calling function cannot be empty.")
        sys.exit(2)

    return call_function, journal, edition


def date_texto(data):
    return str(data.year).zfill(4) + "/" + str(data.month).zfill(2)\
            + "/" + str(data.day).zfill(2)

def date_texto2(data):
    return str(data.day).zfill(2) + "/" + str(data.month).zfill(2)\
            + "/" + str(data.year).zfill(4)

def texto_date(data):
    dia, mes, ano = data.split("/")
    return datetime.date(int(ano), int(mes), int(dia))

def inverter_data(data):
    x, mes, x2 = data.split("/")
    return x2 + "/" + mes + "/" + x


# Verifica se naquele dia deveria haver jornal
def verificar_se_dia_com_jornal(data):

    dia_semana = texto_date(data).weekday()

    if dia_semana == 5 or dia_semana == 6:
        return False
    else:
        return True


# Tenta criar uma pasta temporária
try:
    os.mkdir("jornais")
except:
    pass


if __name__ == "__main__":

    call_function, journal, edition_id = main(sys.argv[1:])

    # Load class reflectively:
    journal_class = locate('journal.' + journal)
    journal = journal_class(edition_id)
