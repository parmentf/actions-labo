import pandas as pd
from unidecode import unidecode
import pickle

"""
Script qui permet de générer un pickle à partir des données fusionnées de la
librairie 'gender_guesser' (https://pypi.org/project/gender-guesser/) et de
Kaggle
(https://www.kaggle.com/datasets/haezer/french-baby-names?select=national_names.csv).
Présentes dans le fichier 'nam_dict_merged.txt'.
"""


with open("nam_dict_merged.txt", "r") as f:
    names = []
    genders = []
    frequencies = []
    for line in f:
        if line[0] not in "#=" and line[29] != "+":
            parts = line.split()
            country_values = line[30:-1]
            name = parts[1]
            name = name.lower()
            name = unidecode(name)
            freq_max = max(country_values)
            names.append(name)
            genders.append(parts[0])
            frequencies.append(freq_max)

    df = pd.DataFrame({"gender": genders, "name": names, "freq": frequencies})
    df = df.sort_values("freq", ignore_index=True)
    df = df.drop_duplicates(subset=["gender", "name"], keep="last", ignore_index=True)
    df = df.drop(columns=["freq"])
    # print(df.to_string())

my_dict = {}
for index, row in df.iterrows():
    my_dict[row["name"].lower()] = row["gender"]
# print(my_dict)


def modified_name_plus(my_dict):
    key_plus = []
    for key in my_dict:
        if "+" in key:
            key_plus.append(key)
    for key in key_plus:
        value = my_dict[key]
        new_key_space = key.replace("+", " ")
        new_key = key.replace("+", "")
        new_key_dash = key.replace("+", "-")
        # ajouter une copie de la paire clé-valeur avec un espace à la fin du
        # dictionnaire
        my_dict[new_key_space] = value
        # ajouter une copie de la paire clé-valeur sans le "+" à la fin du
        # dictionnaire
        my_dict[new_key] = value
        my_dict[new_key_dash] = value
        # supprimer la paire clé-valeur d'origine contenant le "+"
        del my_dict[key]
    return my_dict


def modified_name_apostrophe(my_dict):
    key_apostrophe = []
    for key in my_dict:
        if "'" in key:
            key_apostrophe.append(key)
    for key in key_apostrophe:
        value = my_dict[key]
        new_key = key.replace("'", "")
        # ajouter une copie de la paire clé-valeur sans le "+" à la fin du
        # dictionnaire
        my_dict[new_key] = value
        # supprimer la paire clé-valeur d'origine contenant le "+"
        del my_dict[key]
    return my_dict


my_dict_1 = modified_name_plus(my_dict)
my_dict_modified = modified_name_apostrophe(my_dict_1)
# print(my_dict_modified)

with open("name_gender.pickle", "wb") as handle:
    pickle.dump(my_dict_modified, handle, protocol=pickle.HIGHEST_PROTOCOL)
