import re
from nltk.corpus import stopwords
import spacy

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