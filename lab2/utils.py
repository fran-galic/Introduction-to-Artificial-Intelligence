import os
from typing import List, Optional, Tuple
from data_structures import SkupKazula, Kazula


def ispravna_putanja(putanja, ekstenzija=None):

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


def ucitaj_kazule(mode: str, kazule_path: str) -> Tuple[SkupKazula, Optional[SkupKazula]]:
    if not ispravna_putanja(kazule_path):
        exit(1)

    with open(kazule_path, "r", encoding="utf-8") as file:
        lines = (line.strip() for line in file)
        lines = [line for line in lines if line and not line.startswith("#")]

        print("\n")
        print("Početni ulaz za debugiranje:")
        print(lines)
        print("\n")

        Orginlani_skup = SkupKazula()
        Support_skup = None 

        if mode == "resolution":
            Support_skup = SkupKazula()

        for i, line in enumerate(lines):
            if i + 1 == len(lines) and mode == "resolution":
                zadnja_kazula = Kazula.from_string(line)
                for kazula in zadnja_kazula.negiraj():
                    Support_skup.dodaj_kazulu(kazula)
                continue

            Orginlani_skup.dodaj_kazulu(Kazula.from_string(line))

    return (Orginlani_skup, Support_skup)

def procitaj_ciljanu_kazulu(kazule_path: str) -> Kazula:
    if not ispravna_putanja(kazule_path):
        exit(1)
    
    with open(kazule_path, "r", encoding="utf-8") as file:
        lines = (line.strip() for line in file)
        lines = [line for line in lines if line and not line.startswith("#")]
        return Kazula.from_string(lines[-1])
    
def procitaj_naredbe(naredbe_path: str) -> List[str]:
    if not ispravna_putanja(naredbe_path):
        exit(1)
        
    with open(naredbe_path, "r", encoding="utf-8") as file:
        lines = (line.strip() for line in file)
        lines = [line for line in lines if line and not line.startswith("#")]
    return lines