import spacy
nlp = spacy.load("en_core_web_sm")

def main():
    with open('../Texts/wilson.txt') as text:
        sentences = text.read()
        sentences = sentences.strip()
        sentencelist = sentences.split(".")
        sentencelist.append("Mark Bruijn was a member of The Losers and he was born in 1992.")
        for sentence in sentencelist:
            triple = extract_is_a_rdf_triple(sentence) 
            if triple:
                print(triple)

def extract_is_a_rdf_triple(sentence): 
    tokenlist = []
    entitylist = []
    chunklist = []
    doc = nlp(sentence)

    for ent in doc.ents:
        if ent.label_ == "PERSON":
            entitylist.append(ent.text)

    for chunk in doc.noun_chunks:
        if chunk.root.head.text in ["of"]:
            chunklist.append(str(chunk.root.head.text+" "+chunk.text))

    i = 0
    try:
        for token in doc:
            if token.text in ["is","was"]:
                if doc[i+1].text in ["a","an","the"]:
                    if doc[i+2].pos_ in ["NOUN"]:
                        tokenlist.append(token.text)
                        tokenlist.append(doc[i+1].text)
                        tokenlist.append(doc[i+2].text)
                        tokenlist.append(doc[i+3].text)
            i += 1
    except:
        pass

    if len(entitylist) > 0 and len(tokenlist) > 2:
        if len(chunklist) > 0:
            return((entitylist[0],tokenlist[0]+" "+tokenlist[1],tokenlist[2]+" "+chunklist[0]))
        else:
            return((entitylist[0],tokenlist[0]+" "+tokenlist[1],tokenlist[2]))

if __name__ == '__main__':
    main()