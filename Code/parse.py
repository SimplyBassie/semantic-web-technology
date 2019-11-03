import spacy

def extract_is_a_rdf_triple(doc):
    tokenlist = []
    entitylist = []
    chunklist = []

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
