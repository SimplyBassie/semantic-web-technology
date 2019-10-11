import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
nlp = en_core_web_sm.load()
import sys
import requests
import re

def subtree_matcher(doc, entitylist, labeldic, personlist):
    x = ''
    y = ''
    z = ''
    # iterate through all the tokens in the input sentence
    for i,tok in enumerate(doc):
    # extract subject
        if tok.dep_.find("subjpass") == True:
            y = tok.text
            for nounchunk in entitylist:
                if y.lower() in nounchunk.lower():
                    y = nounchunk

        # extract object
        if tok.dep_.endswith("obj") == True:
            x = tok.text
            for nounchunk in entitylist:
                if x.lower() in nounchunk.lower():
                    x = nounchunk

        # extract ROOT
        if tok.dep_.endswith("ROOT") == True:
            z = tok.text

    if x in labeldic:
        z = z + ": " + labeldic[x]

    if len(y) == 0:
        for person in personlist:
            if person.lower() not in x.lower() and x.lower() not in person.lower():
                y = person
                break
    return y,z,x

sentences = "Adolf Hitler died in Berlin. Adolf Hitler was born in 2000. Adolf Hitler died on October 11, 2019. Adolf Hitler was born in Austria."
sentences = sentences.strip()
sentencelist = sentences.split(".")
for sentence in sentencelist:
    if len(sentence) < 3:
        pass
    else:
        doc = nlp(sentence)
        entitylist = []
        labeldic = {}
        personlist = []
        for word in doc.ents:
            entitylist.append(str(word))
            labeldic[str(word)] = str(word.label_)
            if word.label_ == 'PERSON':
                personlist.append(str(word))
        RDFtriple = subtree_matcher(doc, entitylist, labeldic, personlist)
        print(sentence.strip() + ".")
        print(RDFtriple)
        print()


#https://www.analyticsvidhya.com/blog/2019/09/introduction-information-extraction-python-spacy/
