import conllu
from pprint import pprint

raw_data_cicero = 'cic_att.conllu'
raw_data_caesar = 'caes_gal.conllu'

file = raw_data_cicero


# Open the plain text file for reading; assign under 'data'
with open(file, mode="r", encoding="utf-8") as data:
    # Read the file contents and assign under 'annotations'
    annotations = data.read()

    # annotations = data.readlines()

# Check the type of the resulting object
print(type(annotations))

# Print the first 1000 characters of the string under 'annotations'
# print(annotations[197388:225433])

# with open(output_path, mode="a", encoding="utf-8") as clean_file:
    # Write a new file with only the lines corresponding to the text of Cicero's Epistulae ad Atticum / Caesar's Commentarii Belli Gallici

    # clean_file.writelines(annotations[197388:225433])

#--------------------------------------

# Use the parse() function to parse the annotations; store under 'sentences'
sentences = conllu.parse(annotations)

print(sentences[0]) # this gives us a TokenList object

# Get the metadata for the first item in the list
print(sentences[0].metadata)

# Get the first token in the first sentence
print(sentences[0][0]) #  Just like the TokenList above, the Token is a dictionary-like object with keys and values.

# ---------------------------------------

# x = sentences[1][2:5]
# pprint(x, sort_dicts=False)

# -------------------------------------

def get_ne(sentences:list):
    full_names = []
    for sent in sentences:
        visited_tokens = []
        for token in sent:
            if token['xpos'] == 'Ne' and token not in visited_tokens:
                second_names = [t for t in sent if t['deprel'] == 'flat:name' and t['head'] == token['id'] and t['id'] not in visited_tokens]
                visited_tokens.append(token['id'])
                if second_names:
                    full_names.append([token, [i for i in second_names]])
                else:
                    full_names.append([token])





                # res.append(token) # appends all the details about the token
                # res.append(token['form'])

    return full_names

# for el in get_ne(sentences):
#     for i in el:
#         print(i)


pprint(get_ne(sentences), sort_dicts=False)