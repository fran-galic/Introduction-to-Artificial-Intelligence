from typing import Iterator, List, Tuple
from data_structures import SkupKazula, Kazula

def generiraj_nove_parove(
    support: SkupKazula,
    baza: SkupKazula,
    pocetni_id: int
) -> Iterator[Tuple[Kazula, Kazula]]:
    aktivni_support = sorted([k for k in support.kazule if k.is_active and k.id >= pocetni_id], key=lambda k: k.id)
    aktivni_baza = sorted([k for k in baza.kazule if k.is_active], key=lambda k: k.id)
    svi_support = sorted([k for k in support.kazule if k.is_active], key=lambda k: k.id)

    for k1 in aktivni_support:
        for k2 in aktivni_baza:
            yield (k1, k2)

        for k2 in svi_support:
            if k2.id >= k1.id:
                break
            yield (k1, k2)

def napravi_rezoluciju(k1: Kazula, k2: Kazula) -> SkupKazula:
    novi_skup = SkupKazula()
    zajednicki_parovi = [lit for lit in k1.literali if lit.negirani() in k2.literali]

    if not zajednicki_parovi:
        # ako nemaju zajednickih elementa vrati prazan skup kazula
        return novi_skup

    for lit in zajednicki_parovi:
        novi_literali = (k1.literali | k2.literali) - {lit, lit.negirani()}
        nova_kazula = Kazula(novi_literali)
        nova_kazula.roditelji = (k1.id, k2.id)
        novi_skup.dodaj_kazulu(nova_kazula)

    return novi_skup


def zakljucak_i_ruta(support_skup: SkupKazula, originalna_kazula: Kazula, originalni_skup: SkupKazula):
    nil_kazule = [k for k in support_skup.kazule if len(k.literali) == 0]
    if not nil_kazule:
        print("===============")
        print(f"[CONCLUSION]: {originalna_kazula} is unknown")
        return

    nil = nil_kazule[0]
    sve_kazule = support_skup.kazule + originalni_skup.kazule

    dokazni_lanac = []
    posjeceni = set()

    def prati_do_nil(kazula):
        if kazula.id in posjeceni:
            return
        posjeceni.add(kazula.id)

        if kazula.roditelji:
            r1 = next((k for k in sve_kazule if k.id == kazula.roditelji[0]), None)
            r2 = next((k for k in sve_kazule if k.id == kazula.roditelji[1]), None)
            if r1: prati_do_nil(r1)
            if r2: prati_do_nil(r2)

        dokazni_lanac.append(kazula)

    prati_do_nil(nil)

    print("===============")
    for k in dokazni_lanac:
        if k.roditelji: 
            roditelji_str = f" ({k.roditelji[0]} , {k.roditelji[1]})"
            print(f"{k.id}. {k}{roditelji_str}")
    print("===============")
    print(f"[CONCLUSION]: {originalna_kazula} is true")

def je_vec_poznata(kazula: Kazula, skup: SkupKazula) -> bool:
    for postojeca in skup.kazule:
        if kazula.literali == postojeca.literali:
            return True
    return False

# ideja je vratiti Support skup u kojem smo napravili sve operacije i ukoliko se u njemu nalazi prazna kazula, znaci 
# nasli smo kontradikciju i sve je dokazano, jos je potrebno ispisiati stavri, inace ne
def resolution(Orginalni_skup: SkupKazula, Support_skup: SkupKazula) -> SkupKazula:
    aktivni_id = min([k.id for k in Support_skup.kazule if k.is_active])
    gotovo = False

    while not gotovo:
        new = SkupKazula()

        novi_parovi = generiraj_nove_parove(Support_skup, Orginalni_skup, aktivni_id)
        for k1, k2 in novi_parovi:
            rezolvente = napravi_rezoluciju(k1, k2)
            new.dodaj_skup(rezolvente)

            if any(len(k.literali) == 0 for k in new.kazule):
                Support_skup.dodaj_skup(new)
                return Support_skup

        # ako nismo otkrili nista novo
        # print("stvaranje ukupnog Dosadasnjeg znanja:")
        Dosadasnje_znanje = SkupKazula(Support_skup, Orginalni_skup)
        # print("[DEBUG] Nove kazule:")
        # print(new)
        if all(je_vec_poznata(k, Dosadasnje_znanje) for k in new.kazule):
            gotovo = True
        else:
            Support_skup.dodaj_skup(new)
            aktivni_id = min(k.id for k in new.kazule if k.is_active)

    return Support_skup

def obradi_plus(nova_kazula, korisnicki_dodane, Orginalna_baza, deaktivirane_kazule, zakljucene_kazule):
    print(f"User's command: {str(nova_kazula)} +")
    zakljucene_kazule.clear()
    vec_postoji = False

    for k in korisnicki_dodane:
        if k.literali == nova_kazula.literali:
            k.is_active = True
            vec_postoji = True
            break

    for k in Orginalna_baza.kazule:
        if k.literali == nova_kazula.literali:
            k.is_active = True
            vec_postoji = True
            break

    if not vec_postoji:
        nova_kazula.is_active = True
        korisnicki_dodane.append(nova_kazula)

    deaktivirane_kazule[:] = [k for k in deaktivirane_kazule if k.literali != nova_kazula.literali]
    print(f"Added {str(nova_kazula)}")

def obradi_minus(nova_kazula, korisnicki_dodane, Orginalna_baza, deaktivirane_kazule, zakljucene_kazule):
    print(f"User's command: {str(nova_kazula)} -")
    zakljucene_kazule.clear()
    korisnicki_dodane[:] = [k for k in korisnicki_dodane if k.literali != nova_kazula.literali]

    if any(k.literali == nova_kazula.literali for k in Orginalna_baza.kazule):
        deaktivirane_kazule.append(nova_kazula)
    print(f"Removed {str(nova_kazula)}")

def obradi_upit(nova_kazula, Orginalna_baza, korisnicki_dodane, deaktivirane_kazule, zakljucene_kazule):
    print(f"User's command: {str(nova_kazula)} ?")
    temp_baza = SkupKazula()
    temp_baza.dodaj_skup(Orginalna_baza)
    for k in korisnicki_dodane:
        temp_baza.dodaj_kazulu(k)
    for k in zakljucene_kazule:
        temp_baza.dodaj_kazulu(k)

    for kazula in deaktivirane_kazule:
        for k in temp_baza.kazule:
            if k.literali == kazula.literali:
                k.is_active = False

    support = SkupKazula()
    for neg_kazula in nova_kazula.negiraj():
        support.dodaj_kazulu(neg_kazula)

    support = resolution(temp_baza, support)
    zakljucak_i_ruta(support, nova_kazula, temp_baza)

    for k in korisnicki_dodane + zakljucene_kazule:
        k.is_active = True
    for k in Orginalna_baza.kazule:
        if all(k.literali != d.literali for d in deaktivirane_kazule):
            k.is_active = True

    if any(len(k.literali) == 0 for k in support.kazule):
        if not any(k.literali == nova_kazula.literali for k in Orginalna_baza.kazule + korisnicki_dodane + zakljucene_kazule):
            nova_kazula.is_active = True
            zakljucene_kazule.append(nova_kazula)

def cooking(baza_znanja: SkupKazula, skup_naredbi: List[str]):
    Orginalna_baza = SkupKazula()
    Orginalna_baza.dodaj_skup(baza_znanja)

    korisnicki_dodane: List[Kazula] = []
    zakljucene_kazule: List[Kazula] = []
    deaktivirane_kazule: List[Kazula] = []

    for linija in skup_naredbi:
        print()
        linija = linija.strip()
        if not linija:
            continue

        kazula_str, naredba = linija.rsplit(" ", 1)
        kazula_str = kazula_str.strip()
        naredba = naredba.strip()
        nova_kazula = Kazula.from_string(kazula_str)

        if naredba == "+":
            obradi_plus(nova_kazula, korisnicki_dodane, Orginalna_baza, deaktivirane_kazule, zakljucene_kazule)
        elif naredba == "-":
            obradi_minus(nova_kazula, korisnicki_dodane, Orginalna_baza, deaktivirane_kazule, zakljucene_kazule)
        elif naredba == "?":
            obradi_upit(nova_kazula, Orginalna_baza, korisnicki_dodane, deaktivirane_kazule, zakljucene_kazule)
        else:
            print(f"[ERROR] Nepoznata naredba '{naredba}' u liniji: {linija}")