import pyconll
from pprint import pprint

# This snippet finds sentences where a token marked with part of speech 'AUX' are
# governed by a NOUN. For example, in French this is a less common construction
# and we may want to validate these examples because we have previously found some
# problematic examples of this construction.

raw_data_cicero = 'cic_att.conllu'

train = pyconll.load_from_file(raw_data_cicero)

review_sentences = []
errors = []

names = []

# Conll objects are iterable over their sentences, and sentences are iterable
# over their tokens. Sentences also de/serialize comment information.
for sentence in train:
    visited_names = []
    for token in sentence:

        # Tokens have attributes such as upos, head, id, deprel, etc, and sentences
        # can be indexed by a token's id. We must check that the token is not the
        # root token, whose id, '0', cannot be looked up.
        name = []
        if token.upos == 'PROPN':
            if token.deprel != 'flat:name' and token.head != '0' and sentence[token.head].upos != 'PROPN':
                name_head_id = token.id
                name = [token]
                if name_head_id not in visited_names:
                    name = [tok for tok in sentence if tok.upos == 'PROPN' and tok.deprel == 'flat:name' and sentence[tok.head].id == name_head_id]
                visited_names.append(name_head_id)

        if name:
            names.append(name)


new_names = []
for n in names:
    name_list = []
    for tok in n:
        name_list.append(tok.form)
    new_names.append(name_list)

print(new_names)
