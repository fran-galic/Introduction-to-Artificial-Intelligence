# NAPOMENA: Doslovno sam uzeo svoj kod iz 3. lab vjezbe i prilagodio ga, jer je gotovo identican 
import os

import numpy as np

def provjeri_putanju(putanja, ekstenzija=None):

    if not os.path.exists(putanja):
        print(f"Greška: Putanja '{putanja}' ne postoji.")
        return False
    
    if not os.path.isfile(putanja):
        print(f"Greška: '{putanja}' nije datoteka.")
        return False
    
    if ekstenzija and not putanja.endswith(ekstenzija):
        print(f"Greška: '{putanja}' nije datoteka s ekstenzijom '{ekstenzija}'.")
        return False
    
    return True

def print_data(data):
    X = data["X"]
    y = data["y"]
    feature_names = data["feature_names"]
    target_name = data["target_name"]

    cols = list(zip(*X)) 
    col_widths = [max(len(str(item)) for item in col) for col in cols]
    name_widths = [max(len(feature_names[i]), col_widths[i]) for i in range(len(feature_names))]

    zaglavlje = "  ".join(f"{feature_names[i]:<{name_widths[i]}}" for i in range(len(feature_names)))
    print(zaglavlje)
    print()

    for row in X:
        ispis_reda = "  ".join(f"{row[i]:<{name_widths[i]}}" for i in range(len(row)))
        print(ispis_reda)

    print("\n" + target_name + ":")
    for val in y:
        print(val)

def load_data(path):
    if not provjeri_putanju(path):
        exit(1)

    with open(path, "r", encoding="utf-8") as file:
        lines = [line.strip() for line in file]

        names = lines[0].split(",")
        feature_names = names[0:-1][::-1]
        target_name = names[-1]

        X = [[float(value) for value in line.split(",")[0:-1]][::-1] for line in lines[1:]] 
        y = [float(line.split(",")[-1]) for line in lines[1:]]

        data = {
            "feature_names" : feature_names,
            "target_name" : target_name,
            "X" : X,
            "y" : y
        }

        return data
    
def broj_stupaca_po_elementu(v):
    rezultat = []
    for el in v:
        if isinstance(el, (list, np.ndarray)):
            rezultat.append(len(el))
        else:
            rezultat.append(1)
    return rezultat