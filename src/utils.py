import json
import pickle


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

    return result


if __name__ == "__main__":
    with open("../resources/disease_num2name.p", "rb") as f:
        # Read this dictionary just at the beginning of the program
        search_dictionary = pickle.load(f)

    print(get_subcategories("Hepatitis, Viral, Human", search_dictionary))



