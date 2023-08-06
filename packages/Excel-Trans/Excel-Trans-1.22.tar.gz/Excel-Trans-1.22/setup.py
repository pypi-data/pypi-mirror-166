from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

setup(
    name="Excel-Trans",
    version="1.22",
    author="Quvonchbek Bobojonov",
    author_email="quvonchbek212006@gmail.com",
    description="Excel file format",
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['deep-translator', 'numpy', 'openpyxl', 'pandas'],
    keywords=['python', 'Quvonchbek', 'excel', 'Excel-Trans'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
#twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
