# -*- coding: cp1252 -*-
'''
Created on Jun 9, 2010

@author: coelho
'''

import re
from datetime import datetime
from dateutil.relativedelta import relativedelta

class TxtParser:
    '''
    Classe responsavel por realizar o parse do arquivo txt da fatura de cartoes
    disponibilizada pelo banco do brasil.

    Analizando o arquivo disponibilizado, verifica-se que as linhas que interessam sao as que possuem uma
    data no formato dd/mm no inicio.

    Para cada linha contendo este padrao, vamos extrair as informacoes da seguinte forma:
        date: primeiros 5 caracteres
        desc: do caracter 8 ao 49
        value:
            split no final da linha do 51 caracter em diante, primeiro item
    '''
    items = None
    cardTitle = None #titulo do cartao, definido por "Modalidade" no txt
    cardNumber = None #numero do cartao, definido por Nr.Cartao no txt
    txtFile = None
    dueDate = None #data de vencimento, definido por "Vencimento" no txt

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

        for line in lines:
            self.parseDueDate(line)
            self.parseExchangeRateLine(line)
            self.parseCardTitleLine(line)
            self.parseCardNumberLine(line)

        #now with the exangeRate and dueDate populated, we can parse all transaction lines
        for line in lines:
            self.parseTransactionLine(line)

    def parseDueDate(self, line):
        '''
        popula dueDate se for a linha que representa o vencimento da fatura,
        esta informacao eh utilizada para adivinharmos o ano da compra
        FIXME: ainda pode gerar problemas quando temos uma compra realizada no ano anterior, mas que aparenta ser do ano atual

        '''

        if(line.lstrip().startswith("Vencimento")):
                print "Due date line found. %s" % line

                self.dueDate = datetime.strptime(line.split(":")[1].strip(),'%d.%m.%Y')
                print "Due date is: %s" % self.dueDate


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
            rate = re.findall('X\s+(\S+)', line)[0]
            rate = rate.replace(',','.')
            self.exchangeRate = float(rate)
            print "Exchange Rate value: "+str(self.exchangeRate)
            return self.exchangeRate

        return 0.0


    def parseCardTitleLine(self, line):
        '''
            Titulo do cartao inicia com "Modalidade"
        '''

        if(line.lstrip().startswith("Modalidade")):
                print "Card title line found. %s" % line

                # Fix issue #3 changing from lstrip to strip
                self.cardTitle = line.split(":")[1].strip()
                print "The card title is: %s" % self.cardTitle

    def parseCardNumberLine(self, line):
        '''
            Numero do cartao inicia com "Nr.Cart"
        '''

        if(line.lstrip().startswith("Nr.Cart")):
                print "Card number line found. %s" % line
                # Fix issue #3 changing from lstrip to strip
                self.cardNumber = line.split(":")[1].strip()
                print "The card number is: %s" % self.cardNumber



    def parseTransactionLine(self, line):
        '''
        Linhas de transacao inicial com uma data no formato "dd/mm "
        (devemos verificar o espaco no final pois existem linhas no formato dd/mm/yyyy que nao sao tansacoes)

        caso for uma linha de transacao, um objeto sera adicionado na lista self.items
        este objeto contem os seguintes campos:
            date: data da transacao
            desc: descricao
            value: valor em BRL
        '''

        if(re.match("^\d\d\/\d\d\ $", line[:6]) != None):
            brlValue = ''
            usdValue = ''

            obj = {}
            obj['value'] = self.parseValueFromTransactionLine(line)
            obj['date'] = self.parseDateFromTransactionLine(line)
            obj['desc'] = line[9:48].lstrip().replace('*','')
            obj['fitid'] = (obj['date'] + str(obj['value']) + obj['desc']).replace(' ','')
            print "Line parsed: "+ str(obj)

            # Atualiza data das transacoes de compras parceladas
            self.updateDateFromInstallmentTransactionLine(obj)

            self.items.append(obj)
            return obj

    def parseValueFromTransactionLine(self, line):
        '''
        Extraindo valor da linha, a partir do caracter 51
        Caso esteja em dolar, converter para real utilizando a taxa de cambio.

        Agradecimento especial para Rodrigo que contribuiu pelo code.google
        '''
        value = 0.0

        arr = line[51:].split()

        brlValue = float(arr[0].replace('.','').replace(',','.'))
        usdValue = float(arr[1].replace('.','').replace(',','.'))

        if brlValue != 0.0:
            value = brlValue
        else:
            value = usdValue * self.exchangeRate

        value = value * -1 #inverte valor

        return value

    def parseDateFromTransactionLine(self, line):
        '''
        Extraindo data da linha de transacao
        Como o BB removeu o ano das datas, vamos precisar "adivinhar" o ano correto,
        conforme a data de vencimento

        definimos o ano do vencimento como padrao, porem caso a data da transacao
        fique maior que o vencimento, assumimos o ano anterior como ano correto.

        FIXME transacoes feitas a mais de 12 meses terao o ano definido incorretamente, mas
        nao consegui pensar em outra solucao no momento

        Agradecimento especial a Leonardo F. Cardoso que fez esta contruicao por email. :)
        '''

        transactionDate = datetime.strptime(line[:5],'%d/%m')
        transactionDate = transactionDate.replace(self.dueDate.year)
        if transactionDate >= self.dueDate:
            transactionDate = transactionDate.replace(transactionDate.year-1)

        return transactionDate.strftime('%Y%m%d')

    def updateDateFromInstallmentTransactionLine(self, obj):
        '''
        Verifica se trata-se de uma linha de transacao de compra parcelada (ex.: PARC 01/04) e,
        em caso positivo, posterga o data de vencimento X meses para frente (X = Nro Parc - 1)
        '''        
        regex = re.search("PARC\s\d\d/\d\d", obj['desc']);
        if regex != None:
            installmentNumber = int(regex.group()[5:7])
            originalDate = datetime.strptime(obj['date'], '%Y%m%d')
            newDate = originalDate + relativedelta(months=installmentNumber-1)

            obj['date'] = newDate.strftime('%Y%m%d')
            obj['desc'] = obj['desc'] + " DT ORIG: " + originalDate.strftime('%d/%m')

            print 'Updated installment transaction date. Installment Number: {0} Original: {1} Updated: {2}'.format(installmentNumber, originalDate, newDate)


