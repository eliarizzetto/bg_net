import itertools
from collections import defaultdict
import json

def get_dependency_relations(sentences:list):
    """
    Iterates over every sentence in the text list of Token objects), looks for NE entities in the sentence. Then for
    every pair of NE in the sentence checks if there is an immediate syntactic relation: for any two entities tokens
    that share the same head, are one the head of the other, share the same grandparent head in the tree, or have a
    common node within 2 ancestors tokens, is created a dictionary representing the relation. The dictionary contains
    3 keys: ent1, ent2 and value, corresponding respectively to the two entities and the value (weight) of their
    relation, based on how close they are on the syntactic tree.
    :param sentences: list of sentences represented as list of Token objects
    :return: list of dictionaries representing relations
    """

    global_relations = []
    # all_full_names = []
    for sent in sentences:

        relations_in_sentence = []
        entities_in_sent = []
        visited_tokens = []
        for token in sent:
            if token['upos'] == 'PROPN' and token not in visited_tokens:
                second_names = [t for t in sent if t['deprel'] == 'flat:name' and t['head'] == token['id'] and t not in visited_tokens]
                visited_tokens.append(token)
                if second_names:
                    fullname = [token, *second_names] # the token corresponding to the "first name" at the beginning of the list
                    # all_full_names.append(fullname)
                    entities_in_sent.append(fullname)
                    for t in second_names:
                        visited_tokens.append(t)
                else:
                    fullname = [token]
                    # all_full_names.append(fullname)
                    entities_in_sent.append(fullname)
                    visited_tokens.append(fullname)

        pairs = list(itertools.combinations(entities_in_sent, 2))

        for pair in pairs:
            ent1 = pair[0]
            ent2 = pair[1]
            value = None

            if ent1[0]['head'] == ent2[0]['head']: # same head
                value = 3

            if ent1[0]['head'] == ent2[0]['id'] or ent2[0]['head'] == ent1[0]['id']:
                value = 2

            else:
                try:
                    if ent1[0]['head'] == sent[ent2[0]['head']-1]['head'] or ent2[0]['head'] == sent[ent1[0]['head']-1]['head']:
                        value = 1

                    elif sent[ent1[0]['head']-1]['head'] == sent[ent2[0]['head']-1]['head']: # share grandparent
                        value = 0.5

                except IndexError: # one of the heads is the root
                    value = 0
                    continue


            if value is not None:
                relation = {'ent1':ent1, 'ent2': ent2, 'value': value}
                relations_in_sentence.append(relation)

        if relations_in_sentence:
            global_relations.append(relations_in_sentence)

    return global_relations


def clean_relations_instances(relation_instances: list):
    """
    Cleans the list of dictionaries corresponding to the instances of relations extracted from the text, by removing non-people
    entities, merging the instances of the same relation by summing the weights of each instance, and finally resolving duplicate
    entities deriving from different mentions of the same entity. Returns a list of lists, each of which represents a relation
    between two characters in the text, weighted for the number and quality (closeness in the syntactic tree) of the interactions.
    :param relation_instances: list of dicts
    :return: list of lists
    """
    tmp_relations = []
    for rels_in_sent in relation_instances:

        for rel in rels_in_sent:
            ent1 = ' '.join([i['lemma'] for i in rel['ent1']])
            ent2 = ' '.join([i['lemma'] for i in rel['ent2']])

            value = rel['value']

            row = [ent1, ent2, value]
            tmp_relations.append(row)

    # create a defaultdict to store the sums
    sums = defaultdict(int)

    # loop through the tuples and add the third element to the sum
    # for the corresponding first two elements
    for t in tmp_relations:
        sums[(t[0], t[1])] += t[2]

    # create a new list of lists with the first two elements as the key
    # and the sum as the value
    ne_relations = [[k[0], k[1], v] for k, v in sums.items()]
    ne_relations = [rel for rel in ne_relations if rel[0] != rel[1]]  # remove eventual self-relation

    with open('places.json') as json_file:
        places_list = json.load(json_file)  # assign to a variable the list of all places in Latin literature

    # filter out non-people entities from list
    people_relations = list(filter(lambda x: x[0] not in places_list and x[1] not in places_list, ne_relations))

    # clean duplicate entities
    for idx, item in enumerate(people_relations):
        for i, el in enumerate(item[:2]):
            if 'Cotta' in el:
                item[i] = 'Lucius Aurunculeius Cotta'
                people_relations[idx] = item

    return people_relations