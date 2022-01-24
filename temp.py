from nltk.corpus import treebank_chunk
from nltk.chunk import RegexpParser
from chunkers import sub_leaves
  
from chunkers import PersonChunker
chunker = PersonChunker()
print ("Person name  : ", 
       sub_leaves(chunker.parse(
               treebank_chunk.tagged_sents()[0]), 'PERSON'))