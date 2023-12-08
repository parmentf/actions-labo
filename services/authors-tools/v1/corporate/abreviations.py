import csv
import json


def transform_to_dict(csv_file):
    """
    création du dictionnaire depuis un CSV :
    colonne 1 = key et colonne 2 = value
    """
    my_dict = {}
    with open(csv_file, "r") as file:
        f = csv.reader(file, delimiter="\t")

        for row in f:
            key = row[0].lower().strip()
            value = row[1].lower().strip()
            my_dict[key] = value

    return my_dict


def save_dict_to_json(my_dict, my_json):
    """sauvegarde du dictionnaire dans un json"""
    with open(my_json, "w") as fichier:
        json.dump(my_dict, fichier)


# appel des fonctions
fichier_csv = "abreviations.csv"
resultat = transform_to_dict(fichier_csv)

fichier_json = "abreviations.json"
save_dict_to_json(resultat, fichier_json)
