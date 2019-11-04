import spacy
nlp = spacy.load("en_core_web_sm")

def main():

    with open('../Texts/marshall.txt') as text:
        sentences = text.read()
        sentences = sentences.strip()
        sentencelist = sentences.split(".")
        for sentence in sentencelist:

            bd = birth_death(sentence)
            print(bd)


def birth_death(sentence):
    entitylist = []
    chunklist = []
    datelist = []
    finallist = []
    finallist2 = []
    doc = nlp(sentence)
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


        birthy = " ".join((person_date.split(" ")[:-1]))
        birthy += " birth_year " + person_date.split(" ")[-1][1:5] 

        deathy = " ".join((person_date.split(" ")[:-1]))
        deathy += " death_year " + person_date.split(" ")[-1][-5:-1]

        finallist2.append(birthy)
        finallist2.append(deathy)


    finallist2 = list(set(finallist2))
    return finallist2

        

if __name__ == '__main__':
    main()