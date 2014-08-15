'''
Created on Jun 9, 2010

@author: coelho
'''

import re
from datetime import datetime


class TxtParser:
    '''
    Classe responsavel por realizar o parse do arquivo txt da fatura de cartoes
    disponibilizada pelo banco do brasil.

    Analizando o arquivo disponibilizado, verifica-se que as linhas que interessam sao as que possuem uma
    data no formato dd/mm/yy no inicio.

    Para cada linha contendo este padrao, vamos extrair as informacoes da seguinte forma:
        date: primeiros 8 caracteres
        desc: do caracter 10 ao 49
        value:
            split no final da linha do 51 caracter em diante, primeiro item
    '''
    items = None
    cardTitle = None #name of card, defined by "Modalidade" on txt file
    cardNumber = None #number of card, defined by Nr.Cartao on txt file
    txtFile = None

    def __init__(self,txtFile):
        '''
        Constructor
        '''
        self.items = []
        self.txtFile = txtFile
        self.exchangeRate = 0.0

    def parse(self):
        f = self.txtFile
        lines = f.readlines()

        #before parse transaction lines, we need to load the exchange rate to convert dollar values to real correctly
        #fix issue #5
        for line in lines:
            self.parseExchangeRateLine(line)
            self.parseCardTitleLine(line)
            self.parseCardNumberLine(line)

        #now with the exangeRate populated, we can parse all transaction lines
        for line in lines:
            self.parseTransactionLine(line)

    def parseExchangeRateLine(self, line):
        '''
        popula exchangeRate se for a linha que apresenta o resumo dos gastos
        em dolar. essa linha eh utilizada para extrair o valor da taxa
        de conversao de dolar para real. o que diferencia essa linha da
        linha com o resumo dos gastos em reais a presenca de um sinal
        de multiplicacao (representado por um X)
        '''

        if (re.match('^\s+\S+\s+-\s+\S+\s+\+\s+\S+\s+=\s+\S+\s+X', line)):
            print "Echange Rate line found: "+ line
            self.exchangeRate = float(re.findall('X\s+(\S+)', line)[0])
            print "Exchange Rate value: "+str(self.exchangeRate)
            return self.exchangeRate

        return 0.0


    def parseCardTitleLine(self,line):
        '''
            Card title line starts with "Modalidade"
        '''

        if(line.lstrip().startswith("Modalidade")):
                print "Card title line found. %s" % line

                # Fix issue #3 changing from lstrip to strip
                self.cardTitle = line.split(":")[1].strip()
                print "The card title is: %s" % self.cardTitle

    def parseCardNumberLine(self,line):
        '''
            Card number line starts with "Nr.Cart"
        '''

        if(line.lstrip().startswith("Nr.Cart")):
                print "Card number line found. %s" % line
                # Fix issue #3 changing from lstrip to strip
                self.cardNumber = line.split(":")[1].strip()
                print "The card number is: %s" % self.cardNumber



    def parseTransactionLine(self,line):
        '''
        transction lines starts with a date in the format "dd/mm/yy "
        (we must check with the end space because dates on dd/mm/yyyy format are not a transaction line)

        if that's a transaction line, an parsed object will be append on self.items list,
        this object will contain these fields:
            date: date of transaction
            desc: description
            value: value as BRL
        '''

        if(re.match("^\d\d\/\d\d\/\d\d\ $", line[:9]) != None):
            brlValue = ''
            usdValue = ''

            obj = {}
            obj['date'] = datetime.strptime(line[:8],'%d/%m/%y').strftime('%Y%m%d')
            obj['desc'] = line[9:48].lstrip().replace('*','')

            # LCARD - Start (bugfix issue 2 - country code can have 3 chars, like "BRA" instead of "BR"
            # arr = line[50:].split()
            arr = line[51:].split()
            # LCARD - End (bugfix issue 2 - country code can have 3 chars, like "BRA" instead of "BR"

            brlValue = float(arr[0].replace('.','').replace(',','.')) * -1 #inverte valor
            usdValue = float(arr[1].replace('.','').replace(',','.')) * -1 #inverte valor

            if brlValue != -0.0:
                obj['value'] = brlValue
            else:
                obj['value'] = usdValue * self.exchangeRate

            obj['fitid'] = (obj['date'] + str(obj['value']) + obj['desc']).replace(' ','')

            print "Line parsed: "+ str(obj)
            self.items.append(obj)
            return obj

