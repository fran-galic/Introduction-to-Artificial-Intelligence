import argparse

import algorithms
import heuristics
import utils


def main():
        # učitavanje CLI argumenata
        parser = argparse.ArgumentParser(prog="lab1py", description="1. lab vjezba iz kolegija uuui", epilog="Long Live The King")
        
        parser.add_argument("--alg", choices=["bfs", "ucs", "astar"], help="ucitavanje trazenog algoritma")
        parser.add_argument("--ss", required=True, help= "putanja do datoteke prostora stanja")
        parser.add_argument("--h", help="putanja do heuristike")
        parser.add_argument("--check-optimistic", action="store_true", help="provjera optimističnosti heuristike")
        parser.add_argument("--check-consistent", action="store_true", help="provjera konzistentnosti heuristike")

        args = parser.parse_args()

        # provjera da su unesene odgovarajuće kombinacije parametara
        if not args.alg and not args.check_optimistic and not args.check_consistent:
              print("Morate unjeti ili željeni algoritam ili neku od traženih provjera heuristike (optimalnosti ili konzistentnosti)")
              exit(1)
        
        if (args.alg == "astar" or args.check_optimistic or args.check_consistent) and not args.h:
              print("Za zadanu provjere morate unjesti putanju do heuristike")
              exit(1)

        # prostor stanja sadrzi: begin, goal, transition
        prostor_stanja = utils.load_ss(args.ss)

        if args.alg == "bfs":
              algorithms.bfs(prostor_stanja)
        elif args.alg == "ucs":
              algorithms.ucs(prostor_stanja)
        elif args.alg == "astar":
              algorithms.astar(prostor_stanja, args.h)

        if args.check_optimistic:
              heuristics.optimistic(prostor_stanja, args.h)
        if args.check_consistent:
              heuristics.consistent(prostor_stanja, args.h)         


if __name__ == "__main__":
    main()