from abc import ABC
from ast import literal_eval
from collections import Counter
import enchant
from typing import *
import nltk
import pandas as pd
from pathlib import Path
import random
import re

class LanguageModel(ABC):
  def train(self, text: List[str]):
    raise NotImplemented()
  def generate(self) -> List[str]:
    raise NotImplemented()
  def prob(self, sentence: List[str]) -> float: # get the prob of a sequence
    raise NotImplemented()
  
class NgramLanguageModel(LanguageModel):
  def __init__(self, N, verbose):
    self.ngram_counts = Counter()
    self.n = N
    self.SOS = ['<s>'] * (self.n - 1)
    self.EOS = ['</s>'] * (self.n - 1)
    self.verbose = verbose

  def train(self, text):
    for sent in text:
      tokens = sent.split() # remove traces
      tokens = self.SOS + tokens + self.EOS # Add n-1 EOS and SOS tokens
      self.ngram_counts.update(zip(*[tokens[i:] for i in range(self.n)]))

  def generate(self):
    # Generates a pseudoword, beginning from a SOS token
    result =  self._generate_from_token(self.SOS)[1:]
    return [x[-1] for x in result if x[-1] not in ["<s>", "</s>"]]


  def _generate_from_token(self, token) -> List[str]:
    # # Find all n that starts with token
    if self.verbose:
      print("Generating from: ", token)
    ngrams = [x for x in self.ngram_counts.keys() if x[:self.n - 1] == tuple(token)]
    counts = [self.ngram_counts[x] for x in ngrams]
    unigram_count = sum(counts)
    probs = [x / unigram_count for x in counts]

    # Sample the next token
    ngram = list(random.choices(ngrams, weights=probs)[0])
    if self.verbose:
      print("Selected Ngram: ", ngram)
    if list(ngram[-(self.n - 1):]) == self.EOS: # end of sentence:
      if self.verbose:
        print("EOS Reached")
      return list([ngram[:self.n-1]])
    else:
      # Generate starting with the previously-generated token
      if self.verbose:
        print("Continue generating.")
      result = self._generate_from_token(ngram[-(self.n - 1):])
      return [token] + result

def get_pseudowords(N=1, n_gram=2):
    cwd = Path.cwd()
    parent = Path.cwd()
    # Load the corpus
    # path = '../data/COMBO_Full_ARPA_Aligned.txt'
    path = parent / 'generator/data/COMBO_Full_ARPA_Aligned.txt'

    with open(path, 'r') as f:
        corpus = f.read()
        corpus = corpus.split('\n')

    # Load a dictionary to check if token is a real words or not
    d = enchant.Dict("en_US")

    # Load a corpus of proper nouns to check if tokens are real words or not (pseudowords)
    # path = '../data/Proper_Nouns.txt'
    path = parent / 'generator/data/Proper_Nouns.txt'

    with open(path, 'r') as f:
        proper_nouns = f.read().lower()
        proper_nouns = proper_nouns.split('\n')
    
    ngram_lm = NgramLanguageModel(n_gram, verbose=False)
    ngram_lm.train(corpus)

    # Generate N pseudowords
    pseudowords = []
    pseudowords_set = set()

    tokens_generated = 0
    while tokens_generated < N:
        token = ngram_lm.generate()
        token_tmp = [x.split('_')[0] for x in token]
        pron_tmp = [x.split('_')[1] for x in token]

        if ''.join(token_tmp): # Not an empty token
            # Check if the token is a real word; only include if it is NOT
            if not d.check(''.join(token_tmp)) and ''.join(token_tmp) not in pseudowords_set:
                # Check that the token is not made up of only consonants, and is not a proper noun
                vowels = ["a","e","i","o","u"]
                has_vowel = any(v in ''.join(token_tmp) for v in vowels)
                if has_vowel and (''.join(token_tmp) not in proper_nouns):
                    pseudowords_set.add(''.join(token_tmp))
                    tokens_generated += 1
                    pseudowords += [[''.join(token_tmp)]]

    return pseudowords
            
    
# def main():
#     pseudowords = get_pseudowords(10, 2)
#     print(pseudowords)
    

if __name__ == "__main__": 
    pseudowords = get_pseudowords(10, 2)
    print(pseudowords)
