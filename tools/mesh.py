# Script used to create dictionaries that help to map diseases and drugs to categories
# according to the MeSH
# Most of the code comes from here:
# https://code.tutsplus.com/tutorials/working-with-mesh-files-in-python-linking-terms-and-numbers--cms-28587

import itertools
import pickle
import re

terms = {}
numbers = {}

# meshFile = '/home/haskis/Downloads/d2018.bin'
meshFile = 'd2018.bin'
with open(meshFile, mode='rb') as file:
    mesh = file.readlines()

outputFile = open('mesh.txt', 'w')

for line in mesh:
    meshTerm = re.search(b'MH = (.+)$', line)
    if meshTerm:
        term = meshTerm.group(1)
    meshNumber = re.search(b'MN = (.+)$', line)
    if meshNumber:
        number = meshNumber.group(1)
        numbers[number.decode('utf-8')] = term.decode('utf-8')
        if term in terms:
            terms[term] = terms[term] + ' ' + number.decode('utf-8')
        else:
            terms[term] = number.decode('utf-8')

meshNumberList = []
meshTermList = terms.keys()
for term in meshTermList:
    item_list = terms[term].split(' ')
    for phrase in item_list:
        meshNumberList.append(phrase)

meshNumberList.sort()

used_items = set()
for item in meshNumberList:
    if numbers[item] not in used_items:
        print(numbers[item], '\n', item, file=outputFile)
        used_items.add(numbers[item])
    else:
        print(item, file=outputFile)

print(terms)
filtered_terms = {}

for key, value in terms.items():
    if value[0] != 'C' and value[:3] != 'F03':
        continue
    filtered_terms[key.decode('utf-8')] = value

categories = {}
for n in numbers.keys():
    if n[0] != 'C' and n[:3] != 'F03':
        continue

    term = numbers[n]
    r = categories
    for n_i in n[1:].split('.'):
        if n_i not in r.keys():
            r[n_i] = {}
        r = r[n_i]
    r['name'] = term

# TODO: handle parentheses in Fetishism (Psychiatric), as dialogflow does not allow that
# replaced with "Fetishism Psychiatric", "Fetishism Psychiatric", "Psychiatric Fetishism"
# need to add a "Fetishism Psychiatric" key
with open('disease_name2num.p', 'wb') as f:
    pickle.dump(filtered_terms, f)

with open('disease_num2name.p', 'wb') as f:
    pickle.dump(categories, f)

with open('disease_names.txt', 'w') as f:
    for key, value in filtered_terms.items():
        if value[0] == 'C' or value[:3] == 'F03':
            if ',' not in key:
                f.write('\"%s\", \"%s\"\n' % (key, key))
            else:
                tmp = key.split(',')
                tmp = [s.strip() for s in tmp[::-1]]
                if len(tmp) == 2 or len(tmp) > 4:
                    reversed_no_commas = ' '.join(tmp)
                    f.write('\"%s\", \"%s\", \"%s\"\n' % (key, key, reversed_no_commas))
                else:
                    f.write('\"%s\", \"%s\"' % (key, key))
                    for perm in itertools.permutations(tmp, len(tmp)):
                        f.write(', \"%s\"' % ' '.join(perm))
                    f.write('\n')
