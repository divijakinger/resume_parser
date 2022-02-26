import io
import os
import spacy
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
from spacy.matcher import Matcher
import Convert_file
import extract_email
import extract_mobile_number
from extract_education import extract_education
from extract_name_1 import extract_name_possibility_1
from extract_name_2 import extract_name_possibility_2
from extract_name_3 import extract_name_possibility_3
from extract_skills import extract_skills

file_path = r'D:\Project_Deep_Blue_Archive\Archive\Test_pdfs\1_test.pdf'
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


dir_list = os.listdir(r'D:\Project_Deep_Blue_Archive\Archive')
for name in dir_list:
    file_path = r"D:\Project_Deep_Blue_Archive\Archive\Test_pdfs/6.pdf"
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
    print("Name possibility 3: ", extract_name_possibility_3(text))
    print("Email: ", extract_email.extract_email(text))
    print("Mobile Number: ", extract_mobile_number.extract_mobile_number(text))
    print("Education and Year: ", extract_education(resume_text=text))
    print("Skills: ", extract_skills(resume_text=text))
    break