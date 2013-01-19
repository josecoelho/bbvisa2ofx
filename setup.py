from distutils.core import setup

setup(name = "bbvisa2ofx",
    version = "0.11",
    description = "Converter uma fatura de cartao de credito TXT do Banco do Brasil para OFX",
    author = "Jose Coelho",
    author_email = "contato@josecoelho.com",
    url = "http://josecoelho.com",
    license = "Apache Software License",
    packages = ['bbvisa2ofx'],
    package_dir = {'bbvisa2ofx':'src/bbvisa2ofx'},
    scripts = ["bbvisa2ofx", "bbvisa2ofx_cli"]
)

