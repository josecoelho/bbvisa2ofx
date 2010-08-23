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
            split no final da linha do 50 caracter em diante, primeiro item
        valueUS:
            mesmo split de value, porem segundo item
    '''
    items = None
    cardTitle = None #nome de cartao, definido pela Modalidade no arquivo txt
    file_path = None

    def __init__(self,file_path):
        '''
        Constructor
        '''
        self.items = []
        self.file_path = file_path
        
    def parse(self):
        f = open(self.file_path,'r')
        for line in f.readlines():
            
            if(self.isTransactionLine(line)):
                self.items.append(self.parseTransactionLine(line))
            elif(line.lstrip().startswith("Modalidade")):
                print "Card title line found. %s" % line
                self.cardTitle = line.split(":")[1].lstrip()
                print "The card title is: %s" % self.cardTitle
            
                
                         
    
    def isTransactionLine(self,line):
        '''
        retorna True se a linha comeca com uma
        data no formato "99/99/99 " 
        *o espaco no fim eh necessario pois no inicio do arquivo temos 
        uma data no formato dd/mm/yyyy que nao nos interessa
        '''
        
        if(re.match("^\d\d\/\d\d\/\d\d\ $", line[:9]) != None):
            return True
        return False
    
    def parseTransactionLine(self,line):
        '''
        faz o parse de uma linha retornando um array contendo os campos listados abaixo
        
        date: data da ocorrencia
        desc: descricao da ocorrencia
        value: valor em BRL
        
        
        '''
        obj = {}
        obj['date'] = datetime.strptime(line[:8],'%d/%m/%y').strftime('%Y%m%d')
        obj['desc'] = line[9:48].lstrip()
        arr = line[50:].split()
        obj['value'] = float(arr[0].replace('.','').replace(',','.')) * -1 #inverte valor
        
        print "Line parsed: "+ str(obj)
        return obj