# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

#for facade
#prettytable
#colorama
#protobuf
#grpcio (six)
#pyperclip
#win32com -> pywin32 (!!!)

#MC
#pywhatkit

#for orion
#myssql

#for log
#telegram_send

#for dc2
#docs:
    #mailmerge (pip install docx-mailmerge)
    #xlsxwriter
#ad:
    #pyad
    #pywin32 (!!!)
#transliterate

#for printer (dc2)
#pysnmp

#python setup.py sdist bdist_wheel
#twine upload dist/*
#twine upload --repository-url https://test.pypi.org/legacy/ dist/*
#pip uninstall pih
#pip install --index-url https://test.pypi.org/simple/ pih

# This call to setup() does all the work
setup(
    name="pih",
    version="1.40007",
    description="PIH library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pacifichosp.com/",
    author="Nikita Karachentsev",
    author_email="it@pacifichosp.com",
    license="MIT",
    classifiers=[],
    packages=["pih"],
    include_package_data=True,
    install_requires=["prettytable", "colorama", "protobuf", "grpcio"]
)
