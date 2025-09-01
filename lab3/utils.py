import os

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
        feature_names = names[0:-1]
        target_name = names[-1]

        X = [[value for value in line.split(",")[0:-1]] for line in lines[1:]] 
        y = [line.split(",")[-1] for line in lines[1:]]

        data = {
            "feature_names" : feature_names,
            "target_name" : target_name,
            "X" : X,
            "y" : y
        }

        return data
    
def accuracy(results, golden_marks):
    if (len(results) != len(golden_marks)):
        exit(1)
    total = len(golden_marks)
    correct = len([ x for i, x in enumerate(results) if golden_marks[i] == x ])
    accuracy = correct / total
    return f"{accuracy:.5f}"

def confusion_matrix(predictions, golden_marks):
    print("\n[CONFUSION_MATRIX]:")
    active_features = sorted(list(set(predictions) | set(golden_marks)))
    confusion_matrix = [[0 for _ in active_features ] for _ in active_features]

    for pred, golden in zip(predictions, golden_marks):
        i = active_features.index(golden)
        j = active_features.index(pred)
        confusion_matrix[i][j] += 1

    for i, feature in enumerate(active_features):
        red = " ".join(str(num) for num in confusion_matrix[i])
        print(f"{red}")