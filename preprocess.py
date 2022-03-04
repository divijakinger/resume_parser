import spacy
from spacy.tokens import DocBin

nlp = spacy.blank("en")
import json
import os

combined_data=[]
for line in open('train.json', 'r',encoding='utf-8'):
    combined_data.append(json.loads(line))

training_data=[]

count=0
for data in combined_data:
    try:
        text=data['content']
        temp=[]
        for a in data['annotation']:
            start=a['points'][0]['start']
            end=a['points'][0]['end']
            label=a['label'][0]
            temp.append((start,end,label))
        training_data.append((text,temp))
    except:
        pass


# the DocBin will store the example documents
db = DocBin()
for text, annotations in training_data:
    doc = nlp(text)
    ents = []
    for start, end, label in annotations:
        span = doc.char_span(start, end, label=label)
        ents.append(span)
    doc.ents = ents
    db.add(doc)
db.to_disk("./train.spacy")