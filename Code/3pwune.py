import spacy
import webbrowser

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
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
<script>

$(document).ready(function(){

$('[data-toggle="popover"]').popover({
    html: true
})

});

</script>
</head>
<body>
<div class="container">
<table class="table table-sm">
<tr>
    <th>RDF Triple</th>
</tr>
"""

nlp = spacy.load("en")
printsentencelist = []
dictje = {}

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
            for triple in RDFtriple:
                dictje[triple] = sentence

            for entity, property, property_value in RDFtriple:
                if property_value in labeldic:
                    label = labeldic[property_value]
                else:
                    label = 'X'
                old_property = property
                HTMLTriple = (entity, property, property_value)
                property = property + " (" + label + ")"
                FinalRDFTriple = "<font color='red'>{0}</font>, <font color='green'>{1}</font>, <font color='blue'>{2}</font>".format(entity, property, property_value)
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
                html_page += "<tr data-toggle='popover' data-trigger='hover' title='Original sentence' data-content='{}'><th>{}</th></tr>".format(dictje[HTMLTriple], FinalRDFTriple)
                printsentencelist.append(sentence)
                rdftriplefound = True
                sentence = old_sentence
        if not rdftriplefound:
            sentence += "."
            printsentencelist.append(sentence)

    if printsentencelist[-1] == ".":
        printsentencelist = printsentencelist[:-1]
    html_page += "<table></div>"
    html_page += "<div><h6>" + '"' + (" ").join(printsentencelist) + '"' + "</h6></div>"
    html_page += "<body><html>"
    Html_file= open("output.html","w")
    Html_file.write(html_page)
    Html_file.close()

#filename = 'file:///Users/basgerding/Desktop/semantic-web-technology/Code/' + 'output.html'
#webbrowser.open_new_tab(filename)
