import spacy
import webbrowser

def main():
    nlp = spacy.load("en")
    doc = nlp("Thomas Woodrow Wilson was born on December 28, 1856, in Staunton, Virginia.")
    RDFtriple = extract_rdf(doc)
    print(RDFtriple)

def extract_rdf(doc):
    RDFtriple = []
    spans = list(doc.ents) + list(doc.noun_chunks)
    for span in spans:
        span.merge()
    for ent in doc.ents:
        print("entity:", ent.text)
        preps = [prep for prep in ent.root.head.children]
        for prep in preps:
            print("prep:", prep, prep.dep_)
            for child in prep.children:
                print(ent.text, "{} {}".format(ent.root.text, prep))
                property = "{} {}".format(ent.root.head, prep)
                RDFtriple.append((ent.text, "{} {}".format(ent.root.head, prep), child.text))
    return RDFtriple
if __name__ == '__main__':
    main()
