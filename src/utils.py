import json
import pickle
import numpy as np


def extract_multidim_results(result):
    # No data can be extracted
    if len(result) == 0:
        return None, None, None

    # Dimensionality of the results (How many Fields were used for grouping)
    dim = len(result[0])

    # Extract names of those fields
    keys = []
    for d in range(1, dim):
        keys.append(list(set([r[d] for r in result])))

    # If some dimensions have 1 field just put it to the title
    # Find what dimensions have more than 1 field
    t = []
    new_keys = []
    indices = []
    for i, s in enumerate(keys):
        if len(s) == 1:
            t.append(s[0])
        else:
            new_keys.append(s)
            indices.append(i + 1)

    # If there is nothing to be compared
    if len(new_keys) == 0:
        value = result[0][0]

        # Return title, value and nothing as new keys
        return ', '.join(t), value, new_keys

    else:
        result_array = np.zeros(shape=[len(k) for k in new_keys])
        # Populate results array according to the keys
        for r in result:
            index = []
            value = r[0]
            for d in range(len(new_keys)):
                index.append(new_keys[d].index(r[indices[d]]))
            result_array[tuple(index)] = value

        return ', '.join(t), result_array, new_keys


def get_subcategories(name, search_dict):

    result = []
    def _get_subcategories(name, search_dict, result, append=False):
        if isinstance(search_dict, dict):
            curr_name = search_dict['name'] if 'name' in search_dict.keys() else None
            if curr_name is not None:
                if curr_name == name or append:
                    result.append(curr_name)
                    append = True

            for key, value in search_dict.items():
                _get_subcategories(name, value, result, append)

    _get_subcategories(name, search_dict, result, append=False)

    # Remove duplicates
    return list(set(result))


if __name__ == "__main__":
    with open("../resources/disease_num2name.p", "rb") as f:
        # Read this dictionary just at the beginning of the program
        search_dictionary = pickle.load(f)

    print(get_subcategories("Hepatitis, Viral, Human", search_dictionary))



