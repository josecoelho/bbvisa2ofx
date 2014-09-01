# BBVisa2OFX

This software converts the file of credit card accounts, generated from
Banco do Brasil website, to the OFX format.

You are not from Brazil? So you do not has an account on Banco do Brasil
and this software is useless for you... But if you want a help to
convert a txt file to OFX format (in python), this project would be used
as reference :)

## Portugues-BR:

Este software converte o extrato de cartão de crédito, gerado através do
site do Banco do Brasil, para o formato OFX.

Bem... Eu tenho uma conta no Banco do Brasil e utilizo o GnuCash? para
cuidar das minhas finanças.

Eu sempre exporto os meus extratos para o formato OFX e importo no
GnuCash?. Porém, para o extrato do cartão de credito, VISA no meu caso,
o Banco do Brasil só oferece a opção de exportar para TXT. Então, para
evitar fadiga, eu criei este "script" em python que converte este
arquivo TXT para OFX.

Agora posso importar o extrato do Cartão de credito do Banco do Brasil
no GnuCash? e não perder tempo digitando linha a linha.

Cartoes Master Card tambem sao suportados, e voce pode importar varios
cartoes diferentes que o gnucash vai considerar contas distintas.
(agradecimentos ao Daniel Roviriego)

Mais uma contribuição. Graças ao patch disponibilizado por Rodrigo
Primo, agora o valores em dolar são automaticamente convertidos para
real utilizando a taxa de conversão disponível na fatura.

## INSTALL


```
pip install bbvisa2ofx
```

## Running


With GUI
```
	bbvisa2ofx
```

Commandline
```
    bbvisa2ofx_cli
```


## Development

### Running tests

From root dir exec
```
 python -m bbvisa2ofx.test.txtparser
```

### Publishing a new release (I think it can be done only by me...)

1. increment the version number in your setup.py file,
2. update your CHANGES.txt file,
3. run python setup.py sdist upload again.


WEB Interface
==============

Web Interface on https://github.com/josecoelho/bbvisa2ofx_web


