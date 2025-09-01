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

# učitavanje prostora stanja
def load_ss(ss_path):
    if not provjeri_putanju(ss_path):
        exit(1)

    with open(ss_path, "r", encoding="utf-8") as file:
        lines = (line.strip() for line in file)
        lines = [line for line in lines if not line.startswith("#")]

        begin = lines[0]
        goal =  set(lines[1].split())
        transitions = {}

        for line in lines[2:]:
            main_state = line.split(":")[0]

            state_price_pairs = [state_price for state_price in line.split(":")[1].split()]
            transitions[main_state] = [(pair.split(",")[0], float(pair.split(",")[1])) for pair in state_price_pairs]

        return {
        "begin": begin,
        "goal": goal,
        "transitions": transitions
        }   

    
# učitavanje heuristike
def load_h(h_path):
    if not provjeri_putanju(h_path):
        exit(1)

    with open(h_path, "r", encoding="utf-8") as file:
        lines = (line.strip() for line in file)
        lines = [line for line in lines if not line.startswith("#")]

        heuristic = {}

        for line in lines:
            heuristic[line.split(": ")[0]] = float(line.split(": ")[1])

        return heuristic