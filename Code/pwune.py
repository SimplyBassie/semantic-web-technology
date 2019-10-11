import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
nlp = en_core_web_sm.load()
import sys
import requests
import re

nlp = spacy.load("en_core_web_sm")
personlist = []
entitylist = []
labeldic = {}
with open('../Texts/martin.txt') as text:
    sentence = "Pwune Bruijn was born on September 11, 1998."
    print(sentence)
    wordslist = sentence.split(" ")
    doc = nlp(sentence)
    for word in doc.ents:
        if word.label_ == 'PERSON':
            personlist.append(str(word))
        labeldic[str(word)] = str(word.label_)
        entitylist.append(str(word))

print(entitylist)
print()
#print(wordslist)

for person in personlist:
    for entity in entitylist:
        if person != entity:
            if sentence.index(person) < sentence.index(entity) and (sentence.index(entity) - sentence.index(person)) < 80 :
                property = sentence[(sentence.index(person)+len(person)):sentence.index(entity)]
                person = person.strip()
                property = property.strip()
                entity = entity.strip()
                #if ("born") in property:
                #    property = "birth"
                print("<{0}>\t<{1} ({2})>\t<{3}>".format(person, property, labeldic[entity], entity))





"""
for person in personlist:
    query = '''
    SELECT ?ent WHERE {
    	?ent rdfs:label 'Adolf Hitler'@en.
    	SERVICE wikibase:label {bd:serviceParam wikibase:language 'en' } .
    	}
    '''
    url = 'https://query.wikidata.org/sparql'
    data = requests.get(url, params={'query': query, 'format': 'json'}).json()
    for item in data['results']['bindings']:
        link = (item['ent']['value'])
        answer = link.split("/")[-1]
        print(person, answer)
        break
"""
nounchunklist =  [chunk.text for chunk in doc.noun_chunks]
verblist = [token.lemma_ for token in doc if token.pos_ == "VERB"]
#print("Noun phrases:", [chunk.text for chunk in doc.noun_chunks])
#print("Verbs:", [token.lemma_ for token in doc if token.pos_ == "VERB"])
