import os
import io
import re
from nltk.corpus import stopwords
import spacy
import pdfminer
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

count=0
dir_list = os.listdir('pdf')

def extract_text_from_pdf(pdf_path):
    return extract_text(pdf_path)

for name in dir_list:
    file_path = r"pdf/"+name
    try:
        text = extract_text_from_pdf(file_path)
        name=name.split('.')[0]
        print(name)
        if count<50:
            with open('devashish/'+name+'.txt','w',encoding='utf-8') as f:
                f.writelines(text)
        if 50<=count<100:
            with open('divija/'+name+'.txt','w',encoding='utf-8') as f:
                f.writelines(text)
        if 100<=count<150:
            with open('krishi/'+name+'.txt','w',encoding='utf-8') as f:
                f.writelines(text)
        if 150<=count<200:
            with open('shivam/'+name+'.txt','w',encoding='utf-8') as f:
                f.writelines(text)
        if count>200:
            break
        count+=1
    except:
        pass
    
    