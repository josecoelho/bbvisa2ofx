'''
Created on Jun 9, 2010

@author: coelho
'''
import unittest
from bbvisa2ofx.txtparser import TxtParser
from bbvisa2ofx.bbvisa2ofx import convert
import os, datetime

class Test(unittest.TestCase):
    file_path = os.path.dirname(os.path.abspath(__file__))+"/exemploFaturaCartao.txt";
    parser = ''

    def setUp(self):
        fTxt = open(self.file_path,'r')

        self.parser = TxtParser(fTxt);

    def testParseTransactionLine(self):
        self.parser.dueDate = datetime.datetime(2011,12,25)
        parsedLine = self.parser.parseTransactionLine('11/08    PGTO DEBITO CONTA 3333 000006037  200  211        -1.000,00        0,00')
        self.assertEquals(parsedLine['date'],'20110811')
        self.assertEquals(parsedLine['fitid'],'201108111000.0PGTODEBITOCONTA3333000006037200')
        self.assertEquals(parsedLine['value'],1000.00)
        self.assertEquals(parsedLine['desc'],'PGTO DEBITO CONTA 3333 000006037  200  ')

    def testParseValueFromTransactionLine(self):
        line = '30/07    NETFLIX.COM            SAO PAULO       BR             16,90        0,00'
        value = self.parser.parseValueFromTransactionLine(line)

        self.assertEquals(value, -16.90)

    def testParseValueFromTransactionLine_ConvertingDollarToReal(self):
        line = '25/07    Atlassian              Sydney          AU              0,00       20,00'
        self.parser.exchangeRate = 2 #force exchangeRate
        value = self.parser.parseValueFromTransactionLine(line)

        self.assertEquals(value, -40.00)

    def testParseDateFromTransactionLine_fromSameYear(self):
        line = '25/02    Atlassian              Sydney          AU              0,00       20,00'
        self.parser.dueDate = datetime.datetime(2011,07,25)

        date = self.parser.parseDateFromTransactionLine(line)
        self.assertEquals(date,'20110225')

    def testParseDateFromTransactionLine_guessingYearBefore(self):
        '''
            mesmo mes do vencimento, sugerindo ano anterior
        '''
        line = '25/07    Atlassian              Sydney          AU              0,00       20,00'
        self.parser.dueDate = datetime.datetime(2011,07,25)

        date = self.parser.parseDateFromTransactionLine(line)
        self.assertEquals(date,'20100725')

    def testParse(self):
        self.parser.parse()
        # print self.parser.items
        self.assertEquals(14, len(self.parser.items) )

    def testParse_ConvertingDollarToReal(self):
        self.parser.parse()
        self.assertEquals(-46.86, self.parser.items[1]['value'])

    def testConvert(self):
        fTxt = open(self.file_path,'r')
        fOfx = open(self.file_path+".ofx",'w')

        convert(fTxt,fOfx)

    def testIsDolarLine(self):
        self.assertEquals(self.parser.parseExchangeRateLine('      0,00 -       0,00 +       0,00 =        0,00   X      0.0 =           0,00'),0.0)
        self.assertEquals(self.parser.parseExchangeRateLine('    871,64 -      21,78 +      69,52 =      823,90   X   1.7627 =       1.452,28'),1.7627)
        self.assertEquals(self.parser.parseExchangeRateLine('  1.172,33 -   1.172,33 +   1.039,98 =    1.039,98 -       0,00 =       1.039,98'),0.0)
        self.assertEquals(self.parser.parseExchangeRateLine('    214,17 -     214,79 +     162,00 =      161,38 -       0,00 =         161,3'),0.0)
        self.assertEquals(self.parser.parseExchangeRateLine('11/08/10 TARIFA SOBRE COMPRAS NO EXTERIOR                       0,00        0,44'),0.0)
        self.assertEquals(self.parser.parseExchangeRateLine(''),0.0)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()