'''
Created on Jun 9, 2010

@author: coelho
'''
import unittest
from txtparser import TxtParser
from bbvisa2ofx import convert

class Test(unittest.TestCase):
    file_path = "../testfiles/exemploFaturaCartao.txt";
    parser = ''

    def setUp(self):
        self.parser = TxtParser(self.file_path);

    def testIsTransactionLine(self):
        self.assertTrue(self.parser.isTransactionLine("09/09/09 "));
        self.assertFalse(self.parser.isTransactionLine("09/09asd/09"));
        
    def testParse(self):
        self.parser.parse()
        print self.parser.items    

    def testParse_ConvertingDollarToReal(self):
        self.parser.exchangeRate = 1.7627
        self.parser.parse()
        
        self.assertEquals(-978.26324599999998, self.parser.items[6]['value'])

    def testConvert(self):
        convert(self.file_path,self.file_path+".ofx")
    
    def testIsDolarLine(self):
        self.assertTrue(self.parser.isDolarLine('      0,00 -       0,00 +       0,00 =        0,00   X      0.0 =           0,00'))
        self.assertTrue(self.parser.isDolarLine('    871,64 -      21,78 +      69,52 =      823,90   X   1.7627 =       1.452,28'))
        self.assertFalse(self.parser.isDolarLine('  1.172,33 -   1.172,33 +   1.039,98 =    1.039,98 -       0,00 =       1.039,98'))
        self.assertFalse(self.parser.isDolarLine('    214,17 -     214,79 +     162,00 =      161,38 -       0,00 =         161,3'))
        self.assertFalse(self.parser.isDolarLine('11/08/10 TARIFA SOBRE COMPRAS NO EXTERIOR                       0,00        0,44'))
        self.assertFalse(self.parser.isDolarLine(''))
        
    def testGetExchangeRate(self):
        self.assertEquals(0.0, self.parser.getExchangeRate('      0,00 -       0,00 +       0,00 =        0,00   X      0.0 =           0,00'))
        self.assertEquals(1.7627, self.parser.getExchangeRate('    871,64 -      21,78 +      69,52 =      823,90   X   1.7627 =       1.452,28'))
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()