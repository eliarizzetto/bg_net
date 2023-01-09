import conllu
from pprint import pprint
import networkx as nx

raw_data_cicero = 'cic_att.conllu'
raw_data_caesar = 'caes_gal.conllu'

file = raw_data_caesar



def get_ne(sentences:list):
    full_names = []
    for sent in sentences:
        visited_tokens = []
        for token in sent:
            if token['xpos'] == 'Ne' and token not in visited_tokens:
                second_names = [t for t in sent if t['deprel'] == 'flat:name' and t['head'] == token['id'] and t not in visited_tokens]
                visited_tokens.append(token)
                if second_names:
                    multi_token_name = second_names
                    # multi_token_name.append(token)
                    multi_token_name.insert(0, token) # puts the token corresponding to the "first name" at the beginning of the list
                    full_names.append(multi_token_name)
                    for t in second_names:
                        visited_tokens.append(t)
                else:
                    full_names.append([token])
    return full_names


# Open the plain text file for reading; assign under 'data'
with open(file, mode="r", encoding="utf-8") as data:
    # Read the file contents and assign under 'annotations'
    annotations = data.read()

    sentences = conllu.parse(annotations)

    ne_instances = get_ne(sentences)
    # pprint(get_ne(sentences), sort_dicts=False)


    chars = []
    for l in ne_instances:
        name = [x['lemma'] for x in l]
        chars.append(name)


    first_names = {l[0] for l in chars}

    #print(first_names)



# TODO: capire come processare le relazioni interne all'albero per estrarre collegamenti della forma "N.E.-verbo-N.E.".
#   l'idea è quella di trovare un modo per risalire, da un token all'interno di una frase, ai suoi genitori e nonni.
#       sostanzialmente questa risorsa riassume quello che bisogna fare, che è di base quello che ho già fatto:
#           https://stackoverflow.com/questions/49764862/parsing-conll-u-for-parents-and-grandparents.
