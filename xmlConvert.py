def xml2DictInList(xml):
    new_list_text = xml.split('\n')
    list_dict_text = []
    for i in new_list_text:
        dict_text = {}
        item = i.split(' ')
        for j in item:
            j = j.replace('\"','')
            j = j.split('=')
            if len(j)>1:
                dict_text[j[0]]=j[1]
        if dict_text != {}:
            list_dict_text.append(dict_text)
    return list_dict_text
