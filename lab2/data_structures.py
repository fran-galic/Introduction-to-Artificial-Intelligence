import re
from typing import List, Optional, Set


class Literal:
    def __init__(self, ime: str, negacija: bool = False):
        self.ime = ime.lower()
        self.negacija = negacija

    def __eq__(self, other):
        return isinstance(other, Literal) and self.ime == other.ime and self.negacija == other.negacija

    def __hash__(self):
        return hash((self.ime, self.negacija))

    def __str__(self):
        return f"~{self.ime}" if self.negacija else self.ime

    def negirani(self):
        return Literal(self.ime, not self.negacija)


class Kazula:
    _id_counter = 1

    def __init__(self, literali: Set[Literal]):
        self.literali = set()
        for l in literali:
            if l.negirani() in self.literali:
                # Kazula sama po sebi moze biti tautologija, ali to mozemo detektirati sa je_tautologija() i onda npr. u SkupKazula izbaciti je van
                self.literali.add(l)
                self.literali.add(l.negirani())
            else:
                self.literali.add(l)

        self.id = Kazula._id_counter
        Kazula._id_counter += 1
        self.is_active = True
        self.roditelji: Optional[tuple[int, int]] = None

    def from_string(linija: str) -> 'Kazula':
        literali = set()

        dijelovi = re.split(r'\s+[vV]\s+', linija.strip())

        for dio in dijelovi:
            dio = dio.strip()
            if dio.startswith('~'):
                literali.add(Literal(dio[1:], True))
            else:
                literali.add(Literal(dio, False))

        return Kazula(literali)

    def je_tautologija(self):
        for lit in self.literali:
            if lit.negirani() in self.literali:
                return True
        return False

    def je_podskup_od(self, druga: 'Kazula'):
        return self.literali.issubset(druga.literali)

    def negiraj(self) -> List['Kazula']:
        return [Kazula({lit.negirani()}) for lit in self.literali]

    def __str__(self):
        if len(self.literali) == 0:
            return "NIL"
        else:
            return ' v '.join(str(lit) for lit in self.literali)


class SkupKazula:
    def __init__(self):
        self.kazule: List[Kazula] = []

    def __init__(self, *skupovi: 'SkupKazula'):
        self.kazule: List[Kazula] = []
        for skup in skupovi:
            self.dodaj_skup(skup)

    def dodaj_kazulu(self, nova: Kazula):
        if nova.je_tautologija():
            # print(f"[DEBUG] Odbijena tautologija: {nova}")
            return
        treba_dodati = True
        for kaz in self.kazule:
            if nova.je_podskup_od(kaz):
                kaz.is_active = False
                # print(f"[DEBUG] Nova {nova} je podskup {kaz} → dodajem novu, deaktiviram staru.")
            elif kaz.je_podskup_od(nova):
                nova.is_active = False
                # print(f"[DEBUG] Nova {nova} je nadskup {kaz} → odbacujem novu.")
                treba_dodati = False
                break
        if treba_dodati:
            self.kazule.append(nova)
            # print(f"[DEBUG] Dodana kazula: {nova}")

    def from_spajanje(self, drugi1: 'SkupKazula', drugi2: 'SkupKazula'):
        for k in drugi1.kazule + drugi2.kazule:
            self.dodaj_kazulu(k)

    def je_podskup_od(self, drugi: 'SkupKazula') -> bool:
        aktivne1 = [k for k in self.kazule if k.is_active]
        aktivne2 = [k for k in drugi.kazule if k.is_active]
        return all(any(k1.je_podskup_od(k2) for k2 in aktivne2) for k1 in aktivne1)
    
    def dodaj_skup(self, drugi:'SkupKazula'):
        for k in drugi.kazule:
            self.dodaj_kazulu(k)

    def __str__(self):
        rezultat = []
        for k in self.kazule:
            roditelji_str = f" ({k.roditelji[0]}, {k.roditelji[1]})" if k.roditelji else ""
            status_str = " (X)" if not k.is_active else ""
            rezultat.append(f"{k.id}. {k}{roditelji_str}{status_str}")
        return '\n'.join(rezultat)
