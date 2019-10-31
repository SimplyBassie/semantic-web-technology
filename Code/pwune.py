import spacy
nlp = spacy.load("en_core_web_sm")

def main():
    with open('../Texts/text.txt') as text:
        sentences = text.read()
        sentences = sentences.strip()
        sentencelist_old = sentences.split(".")
        sentencelist = replace_sentences(sentencelist_old)
        for sentence in sentencelist:
            sentence = sentence.strip()
            print(sentence)

def replace_sentences(sentencelist):
    sentencelist2 = []
    for sentence in sentencelist:
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
        sentencelist2.append(new_sentence)
    return sentencelist2

if __name__ == '__main__':
    main()
