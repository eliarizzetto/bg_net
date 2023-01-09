import conllu
from extract_ne import ne_instances
import itertools
from pprint import pprint
from collections import defaultdict


def get_relations(file):
    # Open the plain text file for reading; assign under 'data'
    with open(file, mode="r", encoding="utf-8") as data:
        # Read the file contents and assign under 'annotations'
        annotations = data.read()
        sentences = conllu.parse(annotations)

        ne_tok_instances_set = [l[0] for l in ne_instances]

        global_relations = []
        for s in sentences:  # s = lista di token objects
            relations_in_sentence = []
            ne_in_sentence = list()
            for ent in ne_tok_instances_set:
                if ent in s:
                    ne_in_sentence.append(ent)

            pairs = list(itertools.combinations(ne_in_sentence, 2))

            for pair in pairs:
                ent1 = pair[0]
                ent2 = pair[1]
                distance = None

                if ent1 and ent2 in s:
                    distance = 0.5
                    if ent1['head'] == ent2['head'] or (ent1['head'] == ent2['id'] or ent2['head'] == ent1['id']):
                        distance = 1

                if distance is not None:
                    relation = {'ent1': [ent1], 'ent2': [ent2], 'distance': distance}

                    # disambiguate proper nouns
                    if ent1['lemma'] == ent2['lemma']:
                        second_names_ent1 = [t for t in s if t['head'] == ent1['id'] and t['xpos'] == 'Ne' and t[
                            'deprel'] == 'flat:name']
                        second_names_ent2 = [t for t in s if t['head'] == ent2['id'] and t['xpos'] == 'Ne' and t[
                            'deprel'] == 'flat:name']

                        # if there are no second names, then it's just the same entity mentioned more than once in the sentence --> no relation
                        if not second_names_ent1 and not second_names_ent2:
                            relation = ''
                        # otherwise, add the second names to the list corresponding to the entity
                        else:
                            relation = {'ent1': [ent1, *second_names_ent1], 'ent2': [ent2, *second_names_ent2],
                                        'distance': distance}

                    if relation:
                        relations_in_sentence.append(relation)

            if relations_in_sentence:
                global_relations.append(relations_in_sentence)

        return global_relations



relations = get_relations('caes_gal.conllu')

# pprint(relations)


relations_instances = []
for rels_in_sent in relations:

    for rel in rels_in_sent:

        ent1 = ' '.join([i['lemma'] for i in rel['ent1']])
        ent2 = ' '.join([i['lemma'] for i in rel['ent2']])

        distance = rel['distance']

        row = (ent1, ent2, distance)
        relations_instances.append(row)


# pprint(relations_instances)



# create a defaultdict to store the sums
sums = defaultdict(int)

# loop through the tuples and add the third element to the sum
# for the corresponding first two elements
for t in relations_instances:
    sums[(t[0], t[1])] += t[2]

# create a new list of tuples with the first two elements as the key
# and the sum as the value
final_relations = [(k[0], k[1], v) for k, v in sums.items()]

# print the result
pprint(final_relations)


print(len(final_relations))
