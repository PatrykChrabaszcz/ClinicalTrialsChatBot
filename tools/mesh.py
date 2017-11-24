# Script used to create dictionaries that help to map diseases and drugs to categories
# according to the MeSH
# Most of the code comes from here:
# https://code.tutsplus.com/tutorials/working-with-mesh-files-in-python-linking-terms-and-numbers--cms-28587

import re
import pickle
terms = {}
numbers = {}

meshFile = '/mhome/chrabasp/Download/d2018.bin'
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

filtered_terms = {}

for key, value in terms.items():
    if value[0] != 'D':
        continue
    filtered_terms[key] = value

categories = {}
for n in numbers.keys():
    if n[0] != 'D':
        continue

    term = numbers[n]
    r = categories
    for n_i in n[1:].split('.'):
        if n_i not in r.keys():
            r[n_i] = {}
        r = r[n_i]
    r['name'] = term

# with open('drugs_name2num.p', 'wb') as f:
#     pickle.dump(filtered_terms, f)
#
# with open('drugs_num2name.p', 'wb') as f:
#     pickle.dump(categories, f)

with open('drug_names.txt', 'w') as f:
    for key, value in numbers.items():
        if key[0] == 'D':
            f.write('\"%s\", \"%s\"\n' % (value, value))
