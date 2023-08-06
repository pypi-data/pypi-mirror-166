import argparse
import warnings; warnings.simplefilter('ignore')
import pandas as pd
import spacy
from spacy.symbols import nsubj, nsubjpass, VERB

def rule(doc):
  pairs = []
  for word in doc:
    if word.dep == nsubj or word.dep == nsubjpass:
      if word.head.pos == VERB:
        pairs.append(str(' '.join([word.text, word.head.lemma_])))

      for child in word.children:
        if child.pos == VERB:
          pairs.append(str(' '.join([subject.text, child.lemma_])))

  return pairs

def extract(hansard, col, **kwargs):

  nlp = spacy.load('en_core_web_sm', disable = ['tagger', 'ner', 'attribute_ruler'])
    
  kw = kwargs.get('keep', None)
    
  if kw == 'keep':
    hansard['parsed_text'] = [doc for doc in nlp.pipe(hansard[col].tolist())] # this turns into env
    hansard['subj_verb_pair'] = hansard['parsed_text'].apply(rule)
    hansard = hansard.loc[:, hansard.columns != 'parsed_text']
  else:
    hansard[col] = [doc for doc in nlp.pipe(hansard[col].tolist())] 
    hansard['subj_verb_pair'] = hansard[col].apply(rule)
    hansard = hansard.loc[:, hansard.columns == 'subj_verb_pair']

  hansard = hansard[hansard.astype(str)['subj_verb_pair'] != '[]']

  hansard = hansard.explode('subj_verb_pair')

  return hansard

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  
  parser.add_argument('dataset',
                      help='Name of file to extract triples from.')
  parser.add_argument('col',
                      help='Name of column to extract triples from.')

  args = parser.parse_args()

  extract(args.dataset, args.col)

  #nlp = spacy.load('en_core_web_sm', disable = ['tagger', 'ner', 'attribute_ruler'])
  #out = nlp('She ran to the movies.')
  #rule(out)
