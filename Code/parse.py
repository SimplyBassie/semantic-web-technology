import spacy

nlp = spacy.load("en_core_web_sm")
doc = nlp("Adolf Hitler was born on April 20, 1889. He worked at Apple Inc.")

# ent.text, ent.start_char, ent.end_char, ent.label_

entities = []

for ent in doc.ents:
    entities.append(ent.text)
print(entities)
