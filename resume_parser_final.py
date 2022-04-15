# !pip install -r requirements.txt
# !pip install docx2txt
# !pip install pytesseract
# !pip install pyperclip

import platform, subprocess, tempfile, os, shutil
import sys
from pathlib import Path
from tqdm.auto import tqdm
import re
import pdfkit
import os,os.path
import re
from nltk.corpus import stopwords
import spacy
from spacy.matcher import Matcher
import pandas as pd
import io
import os
import spacy
import docx2txt
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
import cv2
import numpy as np
import requests
import io
import json
import pytesseract
import shutil
import os
import random
import pytesseract as pt
from PIL import Image

#---------------------------------------------------------------------
# Initializations

#Models
nlp_name = spacy.load('en_core_web_sm',disable=['ner','textcat'])
nlp_education = spacy.load('en_core_web_sm')
nlp = spacy.load("./resume_parser")
custom_nlp3 = spacy.load("./company_model/model")
custom_nlp2 = spacy.load("./Degree_model")

# csvs

education = pd.read_csv("degrees_shivam.csv",encoding='unicode_escape',engine='python')
education1=set(education['Full name'])
education2=set(education['abv'])
education1=set([i.lower() for i in education1 if type(i)==str])
education2=set([i.lower() for i in education2 if type(i)==str])
# companies=pd.read_csv('restructured_companies.csv',engine='python')
skills_data_csv = pd.read_csv("skills_superset.csv",engine='python')
job_role_csv = pd.read_csv("roles.csv",engine='python')
job_roles=set(job_role_csv['Job Role'])

#-----------------------------------------------------------------------

"""# Resume Inputs"""

def extract_text_from_docx(filename):
    # extract text
    return docx2txt.process(filename)


def extract_text_from_image_api(filename):
    from PIL import Image
    import pytesseract
    import numpy as np
    from pytesseract import Output


    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    text = pytesseract.image_to_string(filename)
    return text


# def extract_text_from_pdf(filepath):
#     import os
#     import zipfile
#     try:
#         os.remove('output.zip')
#     except:
#         pass
#     extract(filepath)

#     z=zipfile.ZipFile('output.zip')
#     z.extractall('output/')

#     import json

#     with open('output/StructuredData.json','r',encoding='utf-8') as f:
#         data=json.load(f)

#     size=[]
#     final_string=""
#     for ele in data['elements']:
#         try:
#             final_string+=ele['Text']
#             final_string+=' \n '
#         except:
#             pass
#     return final_string

def extract_text_from_pdf(pdf_path):
  import tika
  from tika import parser
  parsedPDF = parser.from_file(pdf_path)
  resume_text = parsedPDF['content']
  return resume_text

"""## Conversion of different file formats to txt"""


def read(filepath):
    try:
        resume_data = ""
        if filepath.endswith("pdf"):
            resume_data=extract_text_from_pdf(filepath)
        elif filepath.endswith("docx"):
            resume_data = extract_text_from_docx(filepath)
        elif (
            filepath.endswith("jpeg")
            or filepath.endswith("jpg")
            or filepath.endswith("png")
        ):
            resume_data = extract_text_from_image_api(filepath)
        elif filepath.endswith("txt"):
            with open(filepath, "r",encoding='utf-8') as f:
                resume_data = f.read()
        else:
            print("Invalid file path")
        return resume_data
    except:
        return 'Invalid Resume'

"""# Name Extraction"""


def next_word(source,target):
  source2 = source.split("\n") 
  for i in source2:
    if target in i:
      return i.strip()

def extract_name(resume_text):
  # create spacy 
  doc = nlp_name(resume_text)
  for token in doc:
      # check token pos
      if token.pos_=='PROPN':
          if token.text.lower() != "curriculum" and token.text.lower() != "vitae"  and token.text.lower() != "resume" :
            # print token
            return(next_word(resume_text,token.text))


"""# Phone Number and Email Extraction"""

"""# Extract Phone Number"""


# Extracting Mobile Number
def extract_mobile_number(text):
    num = re.findall(r"[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]", text)
    try:
        return num[0]
    except:
        return num


"""# Extract Email"""

import re
def extract_email(email):
    email = re.findall("([^@|\s]+@[^@]+\.[^@|\s]+)", email)
    if email:
        try:
            return email[0].split()[0].strip(';')
        except IndexError:
            return None

"""# Education Extraction"""

# def extract_education(text):
#   nlp = spacy.load("./resume_parser")
#   doc = nlp(text)
#   education = {}
#   data={}
#   l=["Address","Certifications","CollegeName","Companies","Designation","Education","Email","Experience","Links","Location","Name","Phone","Projects","Rewards","Skills","Technology"]
#   for key in l: 
#     data[key]=[]
#   try:
#     for ent in doc.ents:
#       data[ent.label_].append(ent.text)
#   except:
#     print()
#   if len(data['Education'])!=0:
#     return data['Education']
#   else:
#     main = []
#     final=['College','University','Institute','Academy']
#     texts=text.split('\n')
#     for t in texts:
#         for f in final:
#             if f.lower() in t.lower():
#                 main.append(t.replace('\n',''))
#     return(main)


def extract_education(text):
    nlp_text_2 = nlp_education(text)
    # removing stop words and implementing word tokenization
    tokens = [token.text for token in nlp_text_2 if not token.is_stop]
    # reading the csv file
    educationset = []
    # check for one-grams (example: python)
    for token in tokens:
      if token.lower() in education1 or token.lower() in education2:
          educationset.append(token)
    # check for bi-grams and tri-grams (example: machine learning)
    for token in nlp_text_2.noun_chunks:
      token = token.text.lower().strip()
      if token.lower() in education1 or token.lower() in education2:
        educationset.append(token)
    return [i.capitalize() for i in set([i.lower() for i in educationset])]

def get_all_educations(resume_text):
  temp=resume_text.split('\n')
  final=[]
  for line in range(len(temp)):
    if len(extract_education(temp[line]))!=0:
      final.append(temp[line]+' '+temp[line+1])
  return final

"""# Companies and Experience Extraction"""

import lexnlp.extract.en.entities.nltk_re

def company_extraction(text):
  doc = custom_nlp3(text)
  degree = []
  degree = [ent.text.replace("\n", " ") for ent in list(doc.ents)]
  if len(list(dict.fromkeys(degree).keys()))!=0:
    return [list(dict.fromkeys(degree).keys()),True]
  else:
    return [list(lexnlp.extract.en.entities.nltk_re.RE_COMPANY.findall(text)),False]



# def company_extraction(text):
#   final=[]
#   data=nlp(text)
#   tokens = [token.text.lower() for token in data if not token.is_stop]
#   for token in tokens:
#     if token[0]=='a':
#         if token in set(companies['A']):
#           final.append(token)
#     elif token[0]=='b':
#         if token in set(companies['B']):
#           final.append(token)
#     elif token[0]=='c':
#         if token in set(companies['C']):
#           final.append(token)
#     elif token[0]=='d':
#         if token in set(companies['D']):
#           final.append(token)
#     elif token[0]=='e':
#         if token in set(companies['E']):
#           final.append(token)
#     elif token[0]=='f':
#         if token in set(companies['F']):
#           final.append(token)
#     elif token[0]=='g':
#         if token in set(companies['G']):
#           final.append(token)
#     elif token[0]=='h':
#         if token in set(companies['H']):
#           final.append(token)
#     elif token[0]=='i':
#         if token in set(companies['I']):
#           final.append(token)
#     elif token[0]=='j':
#         if token in set(companies['J']):
#           final.append(token)
#     elif token[0]=='k':
#         if token in set(companies['K']):
#           final.append(token)
#     elif token[0]=='l':
#         if token in set(companies['L']):
#           final.append(token)
#     elif token[0]=='m':
#         if token in set(companies['M']):
#           final.append(token)
#     elif token[0]=='n':
#         if token in set(companies['N']):
#           final.append(token)
#     elif token[0]=='o':
#         if token in set(companies['O']):
#           final.append(token)
#     elif token[0]=='p':
#         if token in set(companies['P']):
#           final.append(token)
#     elif token[0]=='q':
#         if token in set(companies['Q']):
#           final.append(token)
#     elif token[0]=='r':
#         if token in set(companies['R']):
#           final.append(token)
#     elif token[0]=='s':
#         if token in set(companies['S']):
#           final.append(token)
#     elif token[0]=='t':
#         if token in set(companies['T']):
#           final.append(token)
#     elif token[0]=='u':
#         if token in set(companies['U']):
#           final.append(token)
#     elif token[0]=='v':
#         if token in set(companies['V']):
#           final.append(token)
#     elif token[0]=='x':
#         if token in set(companies['X']):
#           final.append(token)
#     elif token[0]=='y':
#         if token in set(companies['Y']):
#           final.append(token)
#     elif token[0]=='z':
#         if token in set(companies['Z']):
#           final.append(token)
#     else:
#         pass
#   return final,True


def experience_extraction(text):
  doc = nlp(text)
  data={}
  l=["Address","Certifications","CollegeName","Companies","Designation","Education","Email","Experience","Links","Location","Name","Phone","Projects","Rewards","Skills","Technology"]

  for key in l: 
    data[key]=[]
  try:
    for ent in doc.ents:
      data[ent.label_].append(ent.text)
  except:
    print()
  return data['Experience']

def degree_extraction(text):
  doc = custom_nlp2(text)
  degree = []
  degree = [ent.text.replace("\n", " ") for ent in list(doc.ents) if ent.label_ == 'Degree']
  return list(dict.fromkeys(degree).keys())

def extract_skills(resume_text):
    nlp_text_2 = nlp_education(resume_text)
    # removing stop words and implementing word tokenization
    tokens = [token.text for token in nlp_text_2 if not token.is_stop]
    # extract values
    skills_data = set(skills_data_csv.columns.values)
    skillset = []
    # check for one-grams (example: python)
    for token in tokens:
        if token.lower() in skills_data:
            skillset.append(token)
    # check for bi-grams and tri-grams (example: machine learning)
    for token in nlp_text_2.noun_chunks:
        token = token.text.lower().strip()
        if token in skills_data:
            skillset.append(token)
    return [i.capitalize() for i in set([i.lower() for i in skillset])]

def matching(skills_str, skills_taken):
    skills = skills_taken
    count = 0
    skills_list = extract_skills(skills_str)
    skills_list = [i.strip(" ").lower() for i in skills_list]
    length = len(skills_list)
    skills = [i.lower() for i in skills]
    final=set(skills_list).intersection(set(skills))
    try:
      percentage = round(((len(final) / length) * 100))
    except:
      percentage=0
    return percentage

def get_url(text):
  import re
  urls = re.findall(r'(https?://\S+)', text)
  icons=[]
  for url in urls:
    if 'indeed' in url:
      icons.append("https://logos-world.net/wp-content/uploads/2021/02/Indeed-Emblem.png")
    elif 'linkedin' in url:
      icons.append("https://logowik.com/content/uploads/images/linkedin-new4645.jpg")
    elif 'github' in url:
      icons.append("https://www.kindpng.com/picc/m/128-1280187_github-logo-png-github-transparent-png.png")
    elif 'twitter' in url:
      icons.append("https://static01.nyt.com/images/2014/08/10/magazine/10wmt/10wmt-superJumbo-v4.jpg")
    else:
      icons.append('None')
  final={}
  for i in range(len(urls)):
    final[urls[i]]=icons[i]
  return final

def extract_languages(resume_text):
    nlp_text_2 = nlp_education(resume_text)
    # removing stop words and implementing word tokenization
    tokens = [token.text for token in nlp_text_2 if not token.is_stop]
    # reading the csv file
    data = pd.read_csv("Languages.csv")
    # extract values
    skills = data['Language name']
    temp=['south','old','nothern','southern']
    skills=[i.lower().split(' ')[0].replace(';','') for i in skills if i not in temp]
    for t in temp:
      try:
        skills.remove(t)
      except:
        pass
    skillset = []
    # check for one-grams (example: python)
    for token in tokens:
        if token.lower() in skills:
            skillset.append(token)
    return [i.capitalize() for i in set([i.lower() for i in skillset])]

# New Approach of Job Contextual Extraction

import spacy
import os



def extract_job_role(resume_text):
    global job_roles
    global nlp_education
    nlp_text_2 = nlp_education(resume_text)
    # removing stop words and implementing word tokenization
    tokens = [token.text for token in nlp_text_2 if not token.is_stop]
    # reading the csv file
    skillset = []
    # check for one-grams (example: python)
    for token in tokens:
      if token.lower() in job_roles:
          skillset.append(token)
    # check for bi-grams and tri-grams (example: machine learning)
    for token in nlp_text_2.noun_chunks:
      token = token.text.lower().strip()
      if token.lower() in job_roles:
        skillset.append(token)
    return [i.capitalize() for i in set([i.lower() for i in skillset])]

def extract_job_context(resume_text):
  lines=resume_text.split('\n')
  answer=[]
  job_list=[]
  for i in range(len(lines)):
    temp=[]
    final=extract_job_role(lines[i])
    if len(final)!=0:
      job_list.append(final)
      try:
        temp.append(lines[i-1])
      except:
        pass
      temp.append(lines[i])
      try:
        temp.append(lines[i+1])
      except:
        pass
      try:
        temp.append(lines[i+2])
      except:
        pass
      temp=' '.join(temp)
      answer.append(temp)
  return [answer,job_list]

import re
from datetime import date
import os
import logging


def calculate_experience(resume_text):
  def correct_year(result):
      if len(result) < 2:
          if int(result) > int(str(date.today().year)[-2:]):
              result = str(int(str(date.today().year)[:-2]) - 1) + result
          else:
              result = str(date.today().year)[:-2] + result
      return result

  # try:
  experience = 0
  start_month = -1
  start_year = -1
  end_month = -1
  end_year = -1

  not_alpha_numeric = r'[^a-zA-Z\d]'
  number = r'(\d{2})'

  months_num = r'(01)|(02)|(03)|(04)|(05)|(06)|(07)|(08)|(09)|(10)|(11)|(12)'
  months_short = r'(jan)|(feb)|(mar)|(apr)|(may)|(jun)|(jul)|(aug)|(sep)|(oct)|(nov)|(dec)'
  months_long = r'(january)|(february)|(march)|(april)|(may)|(june)|(july)|(august)|(september)|(october)|(november)|(december)'
  month = r'(' + months_num + r'|' + months_short + r'|' + months_long + r')'
  regex_year = r'((20|19)(\d{2})|(\d{2}))'
  year = regex_year
  start_date = month + not_alpha_numeric + r"?" + year
  
  # end_date = r'((' + number + r'?' + not_alpha_numeric + r"?" + number + not_alpha_numeric + r"?" + year + r')|(present|current))'
  end_date = r'((' + number + r'?' + not_alpha_numeric + r"?" + month + not_alpha_numeric + r"?" + year + r')|(present|current|till date|today))'
  longer_year = r"((20|19)(\d{2}))"
  year_range = longer_year + r"(" + not_alpha_numeric + r"{1,4}|(\s*to\s*))" + r'(' + longer_year + r'|(present|current|till date|today))'
  date_range = r"(" + start_date + r"(" + not_alpha_numeric + r"{1,4}|(\s*to\s*))" + end_date + r")|(" + year_range + r")"

  
  regular_expression = re.compile(date_range, re.IGNORECASE)
  
  regex_result = re.search(regular_expression, resume_text)
  
  while regex_result:
    
    try:
      date_range = regex_result.group()
      try:
        
          year_range_find = re.compile(year_range, re.IGNORECASE)
          year_range_find = re.search(year_range_find, date_range)
          replace = re.compile(r"((\s*to\s*)|" + not_alpha_numeric + r"{1,4})", re.IGNORECASE)
          replace = re.search(replace, year_range_find.group().strip())
          start_year_result, end_year_result = year_range_find.group().strip().split(replace.group())
          start_year_result = int(correct_year(start_year_result))
          if (end_year_result.lower().find('present') != -1 or 
              end_year_result.lower().find('current') != -1 or 
              end_year_result.lower().find('till date') != -1 or 
              end_year_result.lower().find('today') != -1): 
              end_month = date.today().month  # current month
              end_year_result = date.today().year  # current year
          else:
              end_year_result = int(correct_year(end_year_result))


      except Exception as e:
          # logging.error(str(e))
          start_date_find = re.compile(start_date, re.IGNORECASE)
          start_date_find = re.search(start_date_find, date_range)

          non_alpha = re.compile(not_alpha_numeric, re.IGNORECASE)
          non_alpha_find = re.search(non_alpha, start_date_find.group().strip())

          replace = re.compile(start_date + r"(" + not_alpha_numeric + r"{1,4}|(\s*to\s*))", re.IGNORECASE)
          replace = re.search(replace, date_range)
          date_range = date_range[replace.end():]
  
          start_year_result = start_date_find.group().strip().split(non_alpha_find.group())[-1]

          start_year_result = int(correct_year(start_year_result))

          if date_range.lower().find('present') != -1 or date_range.lower().find('current') != -1:
              end_month = date.today().month  # current month
              end_year_result = date.today().year  # current year
          else:
              end_date_find = re.compile(end_date, re.IGNORECASE)
              end_date_find = re.search(end_date_find, date_range)

              end_year_result = end_date_find.group().strip().split(non_alpha_find.group())[-1]
              try:
                end_year_result = int(correct_year(end_year_result))
              except Exception as e:
                logging.error(str(e))
                end_year_result = int(re.search("\d+",correct_year(end_year_result)).group())

      if (start_year == -1) or (start_year_result <= start_year):
          start_year = start_year_result
      if (end_year == -1) or (end_year_result >= end_year):
          end_year = end_year_result

      resume_text = resume_text[regex_result.end():].strip()
      regex_result = re.search(regular_expression, resume_text)
    except Exception as e:
      logging.error(str(e))
      resume_text = resume_text[regex_result.end():].strip()
      regex_result = re.search(regular_expression, resume_text)
  # print(start_year, end_year)
  if start_year==-1 and end_year==-1:
    return " "
  else:
    return f"{start_year}-{end_year}"
    

# def extract_all(job_strings,job_list):
#   final=[]
#   for i in range(len(job_strings)):
#     job=job_list[i]
#     experience=calculate_experience(job_strings[i])
#     company=company_extraction(job_strings[i])
#     if len(company)!=0:
#       company=company[0][0]
#       if (job[0]).lower() in company.lower():
#         company=company.lower()
#         company=company.replace((job[0]).lower(),'')
#         company=company.title()
#     print(job,company)
#     if [', '.join(job),experience,company] not in final:
#       final.append([', '.join(job),experience,company])
#   return final

def extract_all(job_strings,job_list,data):
  temp,check=company_extraction(data)

  final=[]
  for i in range(len(job_strings)):
    job=job_list[i]
    experience=calculate_experience(job_strings[i])
    company=''
    if check:
      for c in temp:
        if c in job_strings[i]:
          company=c
          break
    else:
      for c in temp:
        if c[0] in job_strings[i]:
          company=c[0].replace(',','')
          break
    if [', '.join(job),experience,company] not in final:
      final.append([', '.join(job),experience,company])
  return final



def get_degree_2(text):
  doc = custom_nlp2(text)
  degree = []
  degree = [ent.text.replace("\n", " ") for ent in list(doc.ents) if ent.label_ == 'Degree' or ent.label_ == 'Graduation Year']
  return list(dict.fromkeys(degree).keys())

def get_college_2(text):
  doc = custom_nlp2(text)
  degree = []
  degree = [ent.text.replace("\n", " ") for ent in list(doc.ents) if ent.label_ == 'College' or ent.label_ == 'College Name']
  return list(dict.fromkeys(degree).keys())



# Alternative code implemented

def extract_company_context(resume_text):
  lines=resume_text.split('\n')
  answer=[]
  company_list=[]
  for i in range(len(lines)):
    temp=[]
    final=company_extraction(lines[i])
    if len(final)!=0:
      company_list.append(final)
      try:
        temp.append(lines[i-2])
      except:
        pass
      try:
        temp.append(lines[i-1])
      except:
        pass
      temp.append(lines[i])
      try:
        temp.append(lines[i+1])
      except:
        pass
      try:
        temp.append(lines[i+2])
      except:
        pass
      temp=' '.join(temp)
      answer.append(temp)
  return [answer,company_list]

def extract_all_companies_version(company_strings,company_list):
  final=[]
  for i in range(len(company_strings)):
    company=company_list[i]
    experience=calculate_experience(company_strings[i])
    job=extract_job_role(company_strings[i])
    if len(job)!=0:
      final.append([job[0],experience,company])
  return list(set(final))
