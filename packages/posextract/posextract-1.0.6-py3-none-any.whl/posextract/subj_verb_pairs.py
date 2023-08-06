import argparse
import warnings; warnings.simplefilter('ignore')
import pandas as pd
import spacy
from spacy.symbols import nsubj, nsubjpass, VERB

def rule(doc):
  pairs = []
  for word in doc:
    if word.pos == VERB:
      if word.head.dep == nsubj or word.dep == nsubjpass:
        pairs.append(str(' '.join([word.head.lemma_, word.text])))

      for child in word.children:
        if child.dep == nsubj or child.dep == nsubjpass:
          pairs.append(str(' '.join([child.lemma_, word.text])))

  return pairs

def extract(hansard, col, **kwargs):

  nlp = spacy.load('en_core_web_sm', disable = ['ner', 'attribute_ruler'])
    
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
