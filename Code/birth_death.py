import spacy


def birth_death(sentence, doc):
    entitylist = []
    chunklist = []
    datelist = []
    finallist = []
    finallist2 = []
    person_date = ""
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            entitylist.append(ent.text)
            idx = sentence.index(ent.text)
            try:
                person_date = sentence[idx:(idx+len(ent.text)+12)]

            except:
                person = sentence[idx:(idx+len(ent.text))]

        if ent.label_ == "DATE":
            datelist.append(ent.text)

    if person_date[-10:-1] in datelist:
        finallist.append(person_date)


        entity = " ".join((person_date.split(" ")[:-1]))

        RDFtriple = (entity, 'born in (DATE)', person_date.split(" ")[-1][1:5])
        RDFtriple2 = (entity, 'died in (DATE)', person_date.split(" ")[-1][-5:-1])

        finallist2.append(RDFtriple)
        finallist2.append(RDFtriple2)


    finallist2 = list(set(finallist2))
    return finallist2
