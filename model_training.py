import spacy
nlp=spacy.load('en_core_web_sm')

ner=nlp.get_pipe("ner")

import json
import os

f = open('combined.json',encoding='utf-8')
combined_data=json.load(f)

training_data=[]

count=0
for data in combined_data:
    try:
        temp=[]
        for i in data['annotations'][0][1]['entities']:
            temp.append(tuple(i))
        data['annotations'][0][1]['entities']=temp
        final=(data['annotations'][0][0],data['annotations'][0][1])
        training_data.append(final)
    except:
        pass
    




for _, annotations in training_data:
  for ent in annotations.get("entities"):
    ner.add_label(ent[2])

pipe_exceptions = ["ner", "trf_wordpiecer", "trf_tok2vec"]
unaffected_pipes = [pipe for pipe in nlp.pipe_names if pipe not in pipe_exceptions]


# Import requirements
import random
from spacy.training import Example
from spacy.util import minibatch, compounding
from pathlib import Path
import pandas as pd

# TRAINING THE MODEL
with nlp.disable_pipes(*unaffected_pipes):

  # Training for 30 iterations
  for iteration in range(30):

    # shuufling examples  before every iteration
    random.shuffle(training_data)
    losses = {}
    # batch up the examples using spaCy's minibatch
    batches = minibatch(training_data, size=compounding(4.0, 32.0, 1.001))
    for batch in batches:
        texts, annotations = zip(*batch)
    example = []
    # Update the model with iterating each text
    for i in range(len(texts)):
        doc = nlp.make_doc(texts[i])
        example.append(Example.from_dict(doc, annotations[i]))
        # Update the model
        try:
          nlp.update(example, drop=0.5, losses=losses)
        except Exception as error:
          print(error)

        print("Losses", losses)

    
test_text = "ABUBAKRA KHAN f028:  +91 7405524266; +91 8156068986 f03a   abukhank1@gmail.com"
doc = nlp(test_text)
print("Entities", [(ent.text, ent.label_) for ent in doc.ents])
# for ent in doc.ents:
#   print(ent)