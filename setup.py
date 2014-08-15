from distutils.core import setup

setup(name = "bbvisa2ofx",
    version = "0.17b",
    description = "Converter uma fatura de cartao de credito TXT do Banco do Brasil para OFX",
    author = "Jose Coelho",
    author_email = "contato@josecoelho.com",
    url = "http://josecoelho.com",
    license = "Apache Software License",
    packages = ['bbvisa2ofx','bbvisa2ofx.test'],
    package_dir = {'bbvisa2ofx':'bbvisa2ofx'},
    scripts = ["bin/bbvisa2ofx", "bin/bbvisa2ofx_cli"],
    long_description = open('README.md').read()
)

