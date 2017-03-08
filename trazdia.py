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
import subprocess
from subprocess import Popen
import os
import datetime
import pickle
from threading import Thread
import time
from pydoc import locate

from monitor import Monitor
from journal import Journal
from buscador import Buscador


LOGS = []
def documentar(texto):
    global LOGS
    LOGS.append(texto)


# Executa um comando através do SO
def comandar(comando):
    # Faz com que não apareça uma janela de terminal no M$ Windows
    startupinfo = None
    if os.name == 'nt':
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    p = Popen(comando, stderr=subprocess.STDOUT, stdout=subprocess.PIPE,
        startupinfo=startupinfo)
    out, err = p.communicate()
    return (out, err)
#    documentar(out)


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

def montar_nome_arquivo(pasta, data, secao, pagina, extensao):
    return os.path.join(pasta, str(secao) + "_" + str(pagina) + '.' + extensao)


# Converte um arquivo de PDF para texto puro
def converter_pdf(nome_arquivo):
    comandar(["pdftotext", nome_arquivo])


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

    journals = ['Diario_Oficial_Uniao', \
                'Diario_Oficial_SP', \
                'Diario_da_Justica', \
                'Diario_TRF', \
                'Diario_Justica_do_MT', \
                'Diario_Oficial_do_MT']

    monitors = []

    for journal in journals:
        # Load class reflectively:
        journal_class = locate('journal.' + journal)
        m = Monitor(journal_class, "jornais")
        m = m.carregar()
