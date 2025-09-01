import argparse
import utils
from algorithms import ID3


def main():
    parser = argparse.ArgumentParser(prog="lab3py", description="3. lab vjezba iz kolegija uuui", epilog="Long Live The King")

    parser.add_argument("train_path", help="Putanja do datoteke skupa podataka za treniranje")
    parser.add_argument("test_path", help="Putanja do datoteke skupa podataka za testiranje")
    parser.add_argument("max_depth", nargs="?", type=int, default=None, help="Dubina ID3 stabla (opcionalno)")

    args = parser.parse_args()

    train_data = utils.load_data(args.train_path)
    test_data = utils.load_data(args.test_path)

    model = ID3()
    model.fit(train_data, args.max_depth)
    predictions, golden_marks = model.predict(test_data)
    print(f"\n\n[ACCURACY]: {utils.accuracy(predictions, golden_marks)}" )
    utils.confusion_matrix(predictions, golden_marks)


if __name__ == "__main__":
    main()