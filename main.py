import io
import os
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
import Convert_file
import extract_email
import extract_mobile_number
from extract_education import extract_education
from extract_name_1 import extract_name_possibility_1
from extract_name_2 import extract_name_possibility_2


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



# load pre-trained model
nlp = spacy.load('en_core_web_sm')

# initialize matcher with a vocab
matcher = Matcher(nlp.vocab)

def extract_text_from_pdf(pdf_path):
    return extract_text(pdf_path)
resume_text = ""
# Extracting Name
extract_name_possibility_1(resume_text)
extract_name_possibility_2(resume_text)

# Extracting Mobile Number
extract_mobile_number.extract_mobile_number(resume_text)

# Extracting Email
extract_email.extract_email(resume_text)


# load pre-trained model
nlp = spacy.load('en_core_web_sm')
# noun_chunks = nlp.noun_chunks()
doc = nlp(resume_text)
noun_chunks = list(doc.noun_chunks)


# Extracting Skill of the Applicant
def extract_skills(resume_text):
    nlp_text = nlp(resume_text)

    # removing stop words and implementing word tokenization
    tokens = [token.text for token in nlp_text if not token.is_stop]

    # reading the csv file
    data = pd.read_csv("skills.csv")
    skills = list(data.columns.values)

    skillset = []

    # check for one-grams (example: python)
    for token in tokens:
        if token.lower() in skills:
            skillset.append(token)

    # check for bi-grams and tri-grams (example: machine learning)
    for token in noun_chunks:
        token = token.text.lower().strip()
        if token in skills:
            skillset.append(token)

    return [i.capitalize() for i in set([i.lower() for i in skillset])]

# Extract Education
extract_education(resume_text)

dir_list = os.listdir('pdf_test')
for name in dir_list:
    file_path = r"pdf/"+name
    text = ""
    output_path = r"output.pdf"
    print(file_path)
    if file_path.endswith("pdf"):
        # calling above function and extracting text
        for page in extract_text_from_pdf(file_path):
            text += '' + page
    else:
        Convert_file.convert(file_path, output_path)
        # calling above function and extracting text
        for page in extract_text_from_pdf(output_path):
            text += '' + page

    # load pre-trained model
    nlp = spacy.load('en_core_web_sm')
    # noun_chunks = nlp.noun_chunks()
    doc = nlp(text)
    noun_chunks = list(doc.noun_chunks)

    print("Name possibility 1: ", extract_name_possibility_1(text))
    print("Name possibility 2: ", extract_name_possibility_2(text))
    print("Email: ", extract_email.extract_email(text))
    print("Mobile Number: ", extract_mobile_number.extract_mobile_number(text))
    print("Education and Year: ", extract_education(resume_text=text))
    print("Skills: ", extract_skills(resume_text=text))