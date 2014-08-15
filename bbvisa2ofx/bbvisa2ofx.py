
from datetime import datetime
from txtparser import TxtParser

def convert ( fileTxt, fileOfx, closeOfxFile=True):
    """
        fileTxt: python loaded file of txt to be convertedCaminho para o arquivo txt disponibilizado pelo banco do brasil
        fileOfx: python loaded file with path to ofx that will be generated
        closeOfxFile: if false do not close fileOfx on the end of convertion (workaroud to use an StringIO class instead of default file class)
        Em um arquivo OFX temos um banco, que possui contas (neste caso apenas uma) que por sua vez possuem transacoes.
        Os itens retornados pelo parser do txt, representam transacoes de uma conta

        Para cada transacao o parametro FITID eh composto dos valores %(date)%(value)s%(desc) - este item eh preenchido para que o gnucash
        possa defirnir se o item jah foi importado ou nao
    """

    parser = TxtParser(fileTxt)
    parser.parse()
    items = parser.items
    cardTitle = parser.cardTitle
    cardNumber = parser.cardNumber

    today = datetime.now().strftime('%Y%m%d')


    # output
    out=fileOfx

    out.write (
        """OFXHEADER:100
DATA:OFXSGML
VERSION:102
SECURITY:NONE
ENCODING:USASCII
CHARSET:1252
COMPRESSION:NONE
OLDFILEUID:NONE
NEWFILEUID:NON

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
                   <BANKID>%(BANKID)s</BANKID>
                   <ACCTID>%(ACCTID)s</ACCTID>
                   <ACCTTYPE>CHECKING</ACCTTYPE>
                </BANKACCTFROM>
                <BANKTRANLIST>
                    <DTSTART>%(DTSERVER)s</DTSTART>
                    <DTEND>%(DTSERVER)s</DTEND>
        """ % {'DTSERVER':today,'BANKID':cardTitle.replace(' ',''),'ACCTID':cardNumber}
    )

    for item in items:
        out.write(
                """
                    <STMTTRN>
                        <TRNTYPE>OTHER</TRNTYPE>
                        <DTPOSTED>%(date)s</DTPOSTED>
                        <TRNAMT>%(value)s</TRNAMT>
                        <FITID>%(fitid)s</FITID>
                        <MEMO>%(desc)s</MEMO>
                    </STMTTRN>""" % item
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

    if(closeOfxFile):
        out.close()
    print "Success converted"


