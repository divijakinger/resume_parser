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

import Convert_file
import extract_email
import extract_mobile_number
import extract_name_1
import extract_name_2

file_path = r"C:\Users\Devashish Bhake\Documents\Machine Learning A-Z (Codes and Datasets)\Data Science Course\archive\pdf\5.pdf"
text = ""
output_path = r"C:\Users\Devashish Bhake\Documents\Machine Learning A-Z (Codes and Datasets)\Data Science Course\archive\output\sample_git.pdf"


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

if file_path.endswith("pdf"):
    # calling above function and extracting text
    for page in extract_text_from_pdf(file_path):
        text += ' ' + page
else:
    Convert_file.convert(file_path, output_path)
    # calling above function and extracting text
    for page in extract_text_from_pdf(output_path):
        text += ' ' + page

# load pre-trained model
nlp = spacy.load('en_core_web_sm')

# initialize matcher with a vocab
matcher = Matcher(nlp.vocab)

def extract_text_from_pdf(pdf_path):
    return extract_text(pdf_path)
resume_text = ""
# Extracting Name
extract_name_1.extract_name_possibility_1(resume_text)
extract_name_2.extract_name_possibility_2(resume_text)

# Extracting Mobile Number
extract_mobile_number.extract_mobile_number(text)

# Extracting Email
extract_email.extract_email(text)


# load pre-trained model
nlp = spacy.load('en_core_web_sm')
# noun_chunks = nlp.noun_chunks()
doc = nlp(text)
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

# load pre-trained model
nlp = spacy.load('en_core_web_sm')

# Grad all general stop words
STOPWORDS = set(stopwords.words('english'))

# Education Degrees
EDUCATION = [
    'BE', 'B.E.', 'B.E', 'BS', 'B.S', 'B.Sc', 'B.SC', 'BSC', 'BSc',
    'ME', 'M.E', 'M.E.', 'M.Sc', 'M.SC', 'MSC', 'Msc',
    'BTECH', 'B.TECH', 'M.TECH', 'MTECH', 'M.Tech', 'PHD', 'Phd', 'PhD', 'Ph.D',
    '(SSC)', '(HSC)', 'CBSE', 'ICSE', 'X', 'XII', 'Hsc', 'Ssc', '10th', '10TH', '12th', '12TH',
    'SSC', 'HSC','BBA', 'MBA'
]


def extract_education(resume_text):
    nlp_text = nlp(resume_text)

    # Sentence Tokenizer
    nlp_text = [sent.text.strip() for sent in nlp_text.sents]

    edu = {}
    # Extract education degree
    for index, text in enumerate(nlp_text):
        for tex in text.split():
            # Replace all special symbols
            tex = re.sub(r'[?|$|.|!|,|*]', r'', tex)
            if tex.upper() in EDUCATION and tex not in STOPWORDS:
                edu[tex] = text + nlp_text[index + 1]

    # Extract year
    education = []
    for key in edu.keys():
        year = re.search(re.compile(r'(((20|19)(\d{2})))'), edu[key])
        if year:
            education.append((key, ''.join(year[0])))
        else:
            education.append(key)
    return education


print("Name possibility 1: ", extract_name_1.extract_name_possibility_1(text))
print("Name possibility 2: ", extract_name_2.extract_name_possibility_2(text))
print("Email: ", extract_email.extract_email(text))
print("Mobile Number: ", extract_mobile_number.extract_mobile_number(text))
print("Education and Year: ", extract_education(resume_text=text))
print("Skills: ", extract_skills(resume_text=text))
