def translate_property(input_property):
    output_property_found = False
    spacy_label = input_property.split("(")[1]
    spacy_label = spacy_label.split(")")[0]

    #BIRTHPLACE
    birthplace_wordlist = ['born','birth']
    birthplace_spacy_labellist = ['GPE', 'LOC']
    for word in birthplace_wordlist:
        if word in input_property.lower() and spacy_label in birthplace_spacy_labellist:
            output_property = "birthplace"
            output_property_found = True
            break

    #BIRTHDATE
    birthdate_wordlist = ['born','birth']
    birthdate_spacy_labellist = ['DATE']
    for word in birthdate_wordlist:
        if word in input_property.lower() and spacy_label in birthdate_spacy_labellist:
            output_property = "birthdate"
            output_property_found = True
            break

    #DEATHDATE
    deathdate_wordlist = ['die','died','death']
    deathdate_spacy_labellist = ['DATE']
    for word in deathdate_wordlist:
        if word in input_property.lower() and spacy_label in deathdate_spacy_labellist:
            output_property = "deathdate"
            output_property_found = True
            break

    #DEATHPLACE
    deathplace_wordlist = ['die','died','death']
    deathplace_spacy_labellist = ['GPE','LOC']
    for word in deathplace_wordlist:
        if word in input_property.lower() and spacy_label in deathplace_spacy_labellist:
            output_property = "deathplace"
            output_property_found = True
            break



    if output_property_found:
        return True, output_property
    else:
        return False, 'XXX'+input_property+'XXX'
