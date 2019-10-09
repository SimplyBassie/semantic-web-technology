import spacy
from spacy import displacy

nlp = spacy.load("en_core_web_sm")
with open('../Texts/adolf.txt') as text:
    line = text.readline()
    doc = nlp(line)
    #displacy.serve(doc, style="ent")
    displacy.serve(doc, style="dep")
