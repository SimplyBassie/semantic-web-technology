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


html_page = """
<head>
<style>
table {
  font-family: arial, sans-serif;
  border-collapse: collapse;
  width: 100%;
}

td, th {
  border: 1px solid #dddddd;
  text-align: left;
  padding: 8px;
}

tr:nth-child(even) {
  background-color: #dddddd;
}

div{
  text-align: center;
  display: inline-block;
  margin: 0;
  font-style: italic;
}

</style>
</head>
<body>

<h2>RDF Triples:</h2>

<table>
<tr>
    <th>SENTENCE:</th>
    <th>RDF TRIPLE:</th>
</tr>
"""

nlp = spacy.load("en")
printsentencelist = []

with open('../Texts/test.txt') as text:
    sentences = text.read()
    sentences = sentences.strip()
    sentencelist = sentences.split(".")
    for sentence in sentencelist:
        rdftriplefound = False
        sentence = sentence.strip()
        if len(sentence) < 4:
            pass
        else:
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
                if property_value in labeldic:
                    label = labeldic[property_value]
                else:
                    label = 'X'
                old_property = property
                property = property + " (" + label + ")"
                FinalRDFTriple = "<<font color='red'>{0}</font>, <font color='green'>{1}</font>, <font color='blue'>{2}</font>>".format(entity, property, property_value)
                print("\n" + sentence)
                print(entity, property, property_value)
                old_sentence = sentence
                sentence = sentence.replace(entity, "<font color='red'>{}</font>".format(entity))
                if old_property in sentence:
                    sentence = sentence.replace(old_property, "<font color='green'>{}</font>".format(old_property))
                else:
                    new_sentence = ""
                    for word in sentence.split(" "):
                        if word in old_property.split():
                            word = word.replace(word, "<font color='green'>{}</font>".format(word))
                        new_sentence += word
                        new_sentence += " "
                    sentence = new_sentence
                sentence = sentence.replace(property_value, "<font color='blue'>{}</font>".format(property_value))
                sentence = sentence.rstrip()
                sentence += "."
                html_page += "<tr><th>{0}</th><th>{1}</th></tr>".format(sentence, FinalRDFTriple)
                printsentencelist.append(sentence)
                rdftriplefound = True
                sentence = old_sentence
        if not rdftriplefound:
            sentence += "."
            printsentencelist.append(sentence)

    if printsentencelist[-1] == ".":
        printsentencelist = printsentencelist[:-1]
    html_page += "<table><body><html>"
    html_page += "<div><h4>" + '"' + (" ").join(printsentencelist) + '"' + "</h4></div>"
    Html_file= open("output.html","w")
    Html_file.write(html_page)
    Html_file.close()
