import spacy
import webbrowser
from translate_property import translate_property
from parse import extract_instance_of_rdf_triple
from birth_death import birth_death
import sys
nlp = spacy.load("en")

def extract_rdf(doc):
    RDFtriplelist = []
    spans = list(doc.ents) + list(doc.noun_chunks)
    for span in spans:
        span.merge()
    for ent in doc.ents:
        preps = [prep for prep in ent.root.head.children if prep.dep_ == "prep"]
        for prep in preps:
            for child in prep.children:
                property = "{} {}".format(ent.root.head, prep)
                RDFtriplelist.append((ent.text, property, child.text))
    return RDFtriplelist

def replace_sentences(sentencelist):
    sentencelist2 = []
    for sentence in sentencelist:
        sentence = " "+sentence.strip() + " "
        new_sentence = sentence
        doc = nlp(sentence)
        for e in doc.ents:
            if e.label_ == "PERSON":
                replacement = e.text
        for word in sentence.split():
            if word.lower() in ["he","she"]:
                try:
                    new_sentence = sentence.replace(" "+word+" ", " "+replacement+" ")
                except:
                    pass
        sentencelist2.append(new_sentence.strip())
    return sentencelist2

def main():

    hover = False
    button = True

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
    """

    if hover:
        html_page += """
    <table class="table table-sm">
    <tr>
        <th>RDF Triple</th>
    </tr>
    """

    if button:
        html_page += "<br><h3>RDF Triples</h3>"

    printsentencelist = []
    dictje = {}
    x = 0
    with open(sys.argv[1]) as text:
        sentences = text.read()
        sentences = sentences.strip()
        sentencelist = sentences.split(".")
        replaced_sentencelist = replace_sentences(sentencelist)
        sentence_index = 0
        entity_colored = False
        for sentence in sentencelist:
            rdftriplefound = False
            sentence = sentence.strip()
            replaced_sentence = replaced_sentencelist[sentence_index]
            if len(sentence) < 4:
                pass
            else:
                doc = nlp(replaced_sentence)
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
                RDFtriplelist = extract_rdf(doc)
                doc2 = nlp(replaced_sentence)
                RDFtriple_instance_of = extract_instance_of_rdf_triple(doc2)
                if RDFtriple_instance_of != None:
                    RDFtriplelist.append(RDFtriple_instance_of)
                doc3 = nlp(replaced_sentence)
                RDFtriple_birth_death = birth_death(replaced_sentence, doc3)
                RDFtriplelist = RDFtriplelist + RDFtriple_birth_death
                for triple in RDFtriplelist:
                    dictje[triple] = sentence + "."

                for entity, property, property_value in RDFtriplelist:
                    if property_value in labeldic:
                        label = labeldic[property_value]
                    else:
                        label = 'X'
                    old_property = property
                    HTMLTriple = (entity, property, property_value)
                    property = property + " (" + label + ")"
                    propertyfound, property = translate_property(property)
                    #if propertyfound: #FOR PRECISION
                    FinalRDFTriple = "<font color='red'>{0}</font>, <font color='green'>{1}</font>, <font color='blue'>{2}</font>".format(entity, property, property_value)
                    #print("\n" + sentence)
                    #print(entity, property, property_value)
                    old_sentence = sentence
                    sentence2 = sentence.replace(entity, "<font color='red'>{}</font>".format(entity))
                    if sentence2 != sentence:
                        entity_colored = True
                    else:
                        entity_colored = False
                    sentence = sentence2
                    if not entity_colored:
                        sentence = " " + sentence + " "
                        sentence = sentence.replace(" he ", " <font color='red'>{}</font> ".format("he"))
                        sentence = sentence.replace(" He ", " <font color='red'>{}</font> ".format("He"))
                        sentence = sentence.replace(" she ", " <font color='red'>{}</font> ".format("she"))
                        sentence = sentence.replace(" She ", " <font color='red'>{}</font> ".format("She"))
                        sentence = sentence.strip()
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
                    if hover:
                        html_page += "<tr data-toggle='popover' data-trigger='hover' title='Original sentence' data-content='{}'><th>{}</th></tr>".format(dictje[HTMLTriple], FinalRDFTriple)
                    if button:
                        html_page += '''
                        <p>
                          <a class="btn btn-light" data-toggle="collapse" href="#collapseExample{}" role="button" aria-expanded="false" aria-controls="collapseExample{}">
                            {}
                          </a>
                        </p>
                        <div class="collapse" id="collapseExample{}">
                          <div class="card card-body">
                            {}
                          </div>
                        </div>
                        '''.format(str(x),str(x),FinalRDFTriple,str(x),dictje[HTMLTriple])
                        x += 1
                    printsentencelist.append(sentence)
                    rdftriplefound = True
                    sentence = old_sentence
            if not rdftriplefound:
                sentence += "."
                printsentencelist.append(sentence)
            sentence_index += 1

        if printsentencelist[-1] == ".":
            printsentencelist = printsentencelist[:-1]
        html_page += "<table></div>"
        html_page += "<div><h6>" + '"' + (" ").join(printsentencelist) + '"' + "</h6></div>"
        html_page += "<body><html>"
        Html_file= open("output.html","w")
        Html_file.write(html_page)
        Html_file.close()
    print("output.html ready")

        #filename = 'file:///Users/basgerding/Desktop/semantic-web-technology/Code/' + 'output.html'
        #webbrowser.open_new_tab(filename)

if __name__ == '__main__':
    main()
