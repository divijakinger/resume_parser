import spacy
import pandas as pd
resume_text = ""


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
    df = pd.read_csv('skills.csv')

    skills = df['skill']
    skillset = []

    skills = [i.lower() for i in skills]
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