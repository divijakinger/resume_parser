import spacy
from spacy.matcher import Matcher

nlp = spacy.load('en_core_web_sm')

NER = spacy.load("en_core_web_sm", disable=["tok2vec", "tagger", "parser", "attribute_ruler", "lemmatizer"])
# initialize matcher with a vocab
matcher = Matcher(nlp.vocab)
def extract_name_possibility_1(resume_text):
    nlp_text = nlp(resume_text)

    # First name and Last name are always Proper Nouns
    pattern_1 = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]

    matcher.add('NAME', [pattern_1])

    matches = matcher(nlp_text)

    for match_id, start, end in matches:
        span = nlp_text[start:end]
        if 'name' not in span.text.lower():
            if span.text == 'Cirriculum Vitae' or span.text == 'Resume' or span.text == 'Curriculam Vitae' or span.text == 'CURRICULUM VITAE' or span.text == 'CIRRICULAM VITAE':
                continue;
            return span.text