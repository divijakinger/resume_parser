import re
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
file_path = r"C:\Users\Devashish Bhake\Documents\Machine Learning A-Z (Codes and Datasets)\Data Science Course\archive\30_table.doc"
text = ""
output_path = r"C:\Users\Devashish Bhake\Documents\Machine Learning A-Z (Codes and Datasets)\Data Science Course\archive\output\sample.pdf"
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