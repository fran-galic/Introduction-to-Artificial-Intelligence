import argparse
import sys

import utils
import algorithms


def main():
    parser = argparse.ArgumentParser(prog="lab2py", description="2. lab vjezba iz kolegija uuui", epilog="Long Live The King")
    
    parser.add_argument(
        "mode",
        choices=["resolution", "cooking"],
        help="način izvršavanja programa (resolution ili cooking)"
    )
    parser.add_argument(
        "clauses_path",
        help="putanja do popisa kazula"
    )
    parser.add_argument(
        "command_path",
        nargs='?',
        default=None,
        help="putanja do popisa naredbi (samo za 'cooking' način)"
    )
    args = parser.parse_args()

    if args.mode == "cooking" and args.command_path is None:
        print("[GREŠKA] Za 'cooking' način rada morate navesti i command_path.")
        parser.print_usage()
        sys.exit(1)

    if args.mode == "resolution" and args.command_path is not None:
        print("[UPOZORENJE] Za 'resolution' način rada, command_path će biti ignoriran.")

    (Orginlani_skup, Support_skup) = utils.ucitaj_kazule(mode= args.mode, kazule_path= args.clauses_path )
    if args.mode == "resolution":
        Ciljana_kazula = utils.procitaj_ciljanu_kazulu(kazule_path= args.clauses_path)
    if args.mode == "cooking":
        skup_naredbi = utils.procitaj_naredbe(naredbe_path= args.command_path)

    
    print("POCETAK RADA PROGRAMA:")
    print(Orginlani_skup)
    if Support_skup is not None:
        print(Support_skup)

    # glavni dio programa:
    if args.mode == "resolution":
       Support_skup = algorithms.resolution(Orginlani_skup, Support_skup)
       algorithms.zakljucak_i_ruta(support_skup=Support_skup, originalna_kazula=Ciljana_kazula, originalni_skup=Orginlani_skup)
    else:
        algorithms.cooking(baza_znanja= Orginlani_skup, skup_naredbi= skup_naredbi)


if __name__ == "__main__":
    main()