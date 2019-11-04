def translate_property(input_property):
    output_property_found = False
    spacy_label = input_property.split("(")[1]
    spacy_label = spacy_label.split(")")[0]

    #BIRTH_PLACE
    birthplace_wordlist = ['born','birth']
    birthplace_spacy_labellist = ['GPE', 'LOC']
    for word in birthplace_wordlist:
        if word in input_property.lower() and spacy_label in birthplace_spacy_labellist:
            output_property = "birth_place"
            output_property_found = True
            break

    #BIRTH_DATE
    birthdate_wordlist = ['born','birth']
    birthdate_spacy_labellist = ['DATE']
    for word in birthdate_wordlist:
        if word in input_property.lower() and spacy_label in birthdate_spacy_labellist:
            output_property = "birth_date"
            output_property_found = True
            break

    #DEATH_DATE
    deathdate_wordlist = ['die','died','death']
    deathdate_spacy_labellist = ['DATE']
    for word in deathdate_wordlist:
        if word in input_property.lower() and spacy_label in deathdate_spacy_labellist:
            output_property = "death_date"
            output_property_found = True
            break

    #DEATH_PLACE
    deathplace_wordlist = ['die','died','death']
    deathplace_spacy_labellist = ['GPE','LOC']
    for word in deathplace_wordlist:
        if word in input_property.lower() and spacy_label in deathplace_spacy_labellist:
            output_property = "death_place"
            output_property_found = True
            break

    #DEATH_CAUSE
    deathcause_wordlist = ['die of','died of','death of']
    deathcause_spacy_labellist = ['X']
    for word in deathcause_wordlist:
        if word in input_property.lower() and spacy_label in deathcause_spacy_labellist:
            output_property = "death_cause"
            output_property_found = True
            break

    #GRADUATED_PLACE
    graduatedplace_wordlist = ['graduated', 'graduate']
    graduatedplace_spacy_labellist = ['GPE','LOC','ORG']
    for word in graduatedplace_wordlist:
        if word in input_property.lower() and spacy_label in graduatedplace_spacy_labellist:
            output_property = "graduated_place"
            output_property_found = True
            break

    #GRADUATED_DATE
    graduateddate_wordlist = ['graduated', 'graduate']
    graduateddate_spacy_labellist = ['DATE']
    for word in graduateddate_wordlist:
        if word in input_property.lower() and spacy_label in graduateddate_spacy_labellist:
            output_property = "graduated_date"
            output_property_found = True
            break

    #MARRIED_DATE
    marrieddate_wordlist = ['married', 'marry']
    marrieddate_spacy_labellist = ['DATE']
    for word in marrieddate_wordlist:
        if word in input_property.lower() and spacy_label in marrieddate_spacy_labellist:
            output_property = "married_date"
            output_property_found = True
            break

    #DIVORCED_DATE
    divorceddate_wordlist = ['divorced', 'divorce']
    divorceddate_spacy_labellist = ['DATE']
    for word in divorceddate_wordlist:
        if word in input_property.lower() and spacy_label in divorceddate_spacy_labellist:
            output_property = "divorced_date"
            output_property_found = True
            break

    #LIVING_PLACE
    livingplace_wordlist = ['live', 'lives', 'lived', 'resided', 'reside']
    livingplace_spacy_labellist = ['GPE','LOC']
    for word in livingplace_wordlist:
        if word in input_property.lower() and spacy_label in livingplace_spacy_labellist:
            output_property = "living_place"
            output_property_found = True
            break

    #INSTANCE_OF
    is_a_wordlist = ['is a', 'was a', 'is an', 'was an']
    for word in is_a_wordlist:
        if word in input_property.lower():
            output_property = "instance_of"
            output_property_found = True
            break



    if output_property_found:
        return True, output_property
    else:
        return False, input_property.split("(")[0].strip()
