'''
Created on Jun 9, 2010

@author: coelho
'''
import unittest
from txtparser import TxtParser
from bbvisa2ofx import convert

class Test(unittest.TestCase):
    file_path = "/home/coelho/Downloads/faturaCartao (1).txt";

    def testAcceptLine(self):
        parser = TxtParser(self.file_path);
        self.assertTrue(parser.acceptLine("09/09/09 "));
        self.assertFalse(parser.acceptLine("09/09asd/09"));
        
    def testParse(self):
        parser = TxtParser(self.file_path);
        parser.parse()
        print parser.items    


    def testConvert(self):
        convert(self.file_path,"/home/coelho/Downloads/ofxtest.ofx")
    
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()