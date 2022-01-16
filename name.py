
import csv
import re
import spacy
import sys
import pandas as pd
# sys.setdefaultencoding('utf8')
from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import os
import sys, getopt
import numpy as np
from bs4 import BeautifulSoup
import urllib.request
from urllib.request import urlopen
import io
import re
from nltk.corpus import stopwords
import spacy
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
from pdfminer.high_level import extract_text
from spacy.matcher import Matcher
import pandas as pd
import pdfkit
import docx2pdf
import doc2pdf
import win32com.client as win32
from win32com.client import constants
import os,os.path

file_path = r"C:\divija\deepblue\parsing\resume_trial.pdf"
text = ""
output_path = r"C:\divija\deepblue\parsing\output.pdf"

# Extracting Required Texts from the PDF
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as fh:
        # iterate over all pages of PDF document
        for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
            # creating a resource manager
            resource_manager = PDFResourceManager()

            # create a file handle
            fake_file_handle = io.StringIO()

            # creating a text converter object
            converter = TextConverter(
                resource_manager,
                fake_file_handle,
                laparams=LAParams()
            )

            # creating a page interpreter
            page_interpreter = PDFPageInterpreter(
                resource_manager,
                converter
            )

            # process current page
            page_interpreter.process_page(page)

            # extract text
            text = fake_file_handle.getvalue()
            yield text

            # close open handles
            converter.close()
            fake_file_handle.close()


# calling above function and extracting text
for page in extract_text_from_pdf(file_path):
    text += ' ' + page
# print(text)

def extract_name(string):
    r1 = str(string)
    nlp = spacy.load('xx_ent_wiki_sm')
    doc = nlp(r1)
    for ent in doc.ents:
        if(ent.label_ == 'PER'):
            print(ent.text)
            break

extract_name(text)