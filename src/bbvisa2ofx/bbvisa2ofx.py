
from datetime import datetime
from txtparser import TxtParser

def convert ( pathTxt, pathOfx):
    """
        pathTxt: Caminho para o arquivo txt disponibilizado pelo banco do brasil
        pathOfx: Caminho para o arquivo a ser gerado
        
        Em um arquivo OFX temos um banco, que possui contas (neste caso apenas uma) que por sua vez possuem transacoes.
        Os itens retornados pelo parser do txt, representam transacoes de uma conta 
    """
    
    parser = TxtParser(pathTxt)
    
    items = parser.parse()
    
    today = datetime.now().strftime('%Y%m%d')
    
    
    # output
    out=open(pathOfx,'w')
    
    out.write (
        """
        <OFX>
            <SIGNONMSGSRSV1>
                <SONRS>
                    <STATUS>
                        <CODE>0</CODE>
                        <SEVERITY>INFO</SEVERITY>
                    </STATUS>
                    <DTSERVER>%(DTSERVER)s</DTSERVER>
                    <LANGUAGE>POR</LANGUAGE>
                    <FI>
                        <ORG>Banco do Brasil</ORG>
                        <FID>1</FID>
                    </FI>
                </SONRS>
            </SIGNONMSGSRSV1>
            <BANKMSGSRSV1>
                <STMTTRNRS>
                    <TRNUID>1</TRNUID>
                    <STATUS>
                        <CODE>0</CODE>
                        <SEVERITY>INFO</SEVERITY>
                    </STATUS>
                    <STMTRS>
                        <CURDEF>BRL</CURDEF>
                        <BANKACCTFROM>
                           <BANKID>VISA BB</BANKID>
                           <ACCTTYPE>CHECKING</ACCTTYPE>
                        </BANKACCTFROM>
                        <BANKTRANLIST>
                            <DTSTART>%(DTSERVER)s</DTSTART>
                            <DTEND>%(DTSERVER)s</DTEND>
        """ % {'DTSERVER':today}
    )
        
    for item in items:
        out.write(
            """
                            <STMTTRN>
                                <TRNTYPE>OTHER</TRNTYPE>
                                <DTPOSTED>%(date)s</DTPOSTED>
                                <TRNAMT>%(value)s</TRNAMT>
                                <MEMO>%(desc)s</MEMO>
                            </STMTTRN> 
            """ % item     
                  )
    
    
    
    out.write(
        """
                        </BANKTRANLIST>
                        <LEDGERBAL>
                            <BALAMT>0</BALAMT>
                            <DTASOF>%s</DTASOF>
                        </LEDGERBAL>
                    </STMTRS>
                </STMTTRNRS>
            </BANKMSGSRSV1>
        </OFX>
        """ % today
              
              
    )
    
    out.close()
    print "Exported %s" % pathOfx