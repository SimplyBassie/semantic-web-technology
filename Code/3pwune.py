import spacy

def extract_rdf(doc):
    RDFtriple = []
    spans = list(doc.ents) + list(doc.noun_chunks)
    for span in spans:
        span.merge()
    for ent in doc.ents:
        preps = [prep for prep in ent.root.head.children if prep.dep_ == "prep"]
        for prep in preps:
            for child in prep.children:
                RDFtriple.append((ent.text, "{} {}".format(ent.root.head, prep), child.text))
    return RDFtriple


nlp = spacy.load("en")

sentences = """
Adolf Hitler was born in Austria.
In 1999 Hitler was born.
Hitler died on October 11, 2019.
In Germany, Adolf Hitler died.
Barrack Obama was born in Hawaii in the year 1961.
Adolf Hitler was born on April 20, 1889, in Austria.
Thomas Woodrow Wilson was born in America on December 28, 1856.
"""

sentences = sentences.strip()
sentencelist = sentences.split(".")
for sentence in sentencelist:
    sentence = sentence.strip()
    if len(sentence) < 1:
        pass
    else:
        print("\n'" + sentence + ".'")
        doc = nlp(sentence)
        nounchunklist = [str(chunk.text).strip() for chunk in doc.noun_chunks]
        entitylist = []
        labeldic = {}
        personlist = []
        lemmadic = {}
        for word in doc.ents:
            entitylist.append(str(word))
            labeldic[str(word)] = str(word.label_)
            lemmadic[str(word)] = str(word.lemma_)
            if word.label_ == 'PERSON':
                personlist.append(str(word))
        RDFtriple = extract_rdf(doc)
        for entity, property, property_value in RDFtriple:
            label = labeldic[property_value]
            property = property + " (" + label + ")"
            FinalRDFTriple = (entity, property, property_value)
            print(FinalRDFTriple)
