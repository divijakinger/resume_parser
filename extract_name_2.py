import spacy
from spacy.matcher import Matcher
nlp = spacy.load('en_core_web_sm')
NER = spacy.load("en_core_web_sm", disable=["tok2vec", "tagger", "parser", "attribute_ruler", "lemmatizer"])
matcher = Matcher(nlp.vocab)


def extract_name_possibility_2(resume_text):
    nlp_text_2 = nlp(resume_text)

    # First name and Last name are always Proper Nouns
    pattern_2 = [{'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}]
    matcher.add('NAME', [pattern_2])

    matches_2 = matcher(nlp_text_2)

    for match_id, start, end in matches_2:
        span2 = nlp_text_2[start:end]
        if 'name' not in span2.text.lower():
            if span2.text == 'Cirriculum Vitae' or span2.text == 'Resume' or span2.text == 'Curriculam Vitae' or span2.text == 'CURRICULUM VITAE' or span2.text == 'CIRRICULAM VITAE':
                continue;
            return span2.text
