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

def change_word_format(file_path):
    word = win32.gencache.EnsureDispatch('Word.Application')
    doc = word.Documents.Open(file_path)
    doc.Activate()

    # Rename path with .doc
    new_file_abs = os.path.abspath(file_path)
    new_file_abs = re.sub(r'\.\w+$', '.doc', new_file_abs)

    # Save and Close
    word.ActiveDocument.SaveAs(
        new_file_abs, FileFormat=constants.wdFormatDocument
    )
    doc2pdf.convert(new_file_abs, output_path)
    doc.Close(False)
# !!!!! Only Change This for Testing docx and pdf execution !!!!!
# Converting the Docx Files to PDF for faster execution
file_path = r"C:\divija\deepblue\project_deep_blue\resumes_database\resume_5.pdf"
text = ""
output_path = r"C:\divija\deepblue\output.pdf"

# convert docx to pdf
if file_path.endswith(".docx"):
    docx2pdf.convert(file_path, output_path)

# convert html to pdf
elif file_path.endswith(".html"):
    config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")
    kitoptions = {
        "enable-local-file-access": None
    }
    pdfkit.from_file(file_path, output_path, configuration=config, options=kitoptions)

# convert rtf to pdf
elif file_path.endswith(".rtf"):
    change_word_format(file_path)

# convert doc to pdf
elif file_path.endswith(".doc"):
    doc2pdf.convert(file_path, output_path)

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

#spacy.cli.download("en_core_web_sm")

# nlp = spacy.load("en_core_web_sm")


# load pre-trained model
nlp = spacy.load('en_core_web_sm')

NER = spacy.load("en_core_web_sm", disable=["tok2vec", "tagger", "parser", "attribute_ruler", "lemmatizer"])
# initialize matcher with a vocab
matcher = Matcher(nlp.vocab)

def extract_text_from_pdf(pdf_path):
    return extract_text(pdf_path)

# Extracting Name

def extract_name(resume_text):
    nlp_text = nlp(resume_text)

    # First name and Last name are always Proper Nouns
    pattern = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]

    matcher.add('NAME', [pattern])

    matches = matcher(nlp_text)

    for match_id, start, end in matches:
        span = nlp_text[start:end]
        if 'name' not in span.text.lower():
            if span.text == 'Cirriculum Vitae' or span.text == 'Resume' or span.text == 'Curriculam Vitae' or span.text == 'CURRICULUM VITAE' or span.text == 'CIRRICULAM VITAE':
                continue
            return span.text



# Extracting Mobile Number
def extract_mobile_number(text):
    phone = re.findall(re.compile(
        r'(?:(?:\+?([1-9]|[0-9][0-9]|[0-9][0-9][0-9])\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([0-9][1-9]|[0-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?'),
        text)

    if phone:
        number = ''.join(phone[0])
        if len(number) >= 10:
            return '+' + number
        else:
            return number


# Extracting Email
def extract_email(email):
    email = re.findall("([^@|\s]+@[^@]+\.[^@|\s]+)", email)
    if email:
        try:
            return email[0].split()[0].strip(';')
        except IndexError:
            return None


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
    data1 = pd.read_csv("skills.csv")
    data2 = pd.read_csv("skills_db.csv")
    data = data1.append(data2)
    # extract values
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


# nltk.download('stopwords')
# nltk.download('words')

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
    'SSC', 'HSC','BBA'
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


print("Name: ", extract_name(text))
print("Email: ", extract_email(text))
print("Mobile Number: ", extract_mobile_number(text))
print("Education and Year: ", extract_education(resume_text=text))
# print("Skills: ", extract_skills(resume_text=text))
