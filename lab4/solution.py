import argparse
import utils
from NeuralNet import NeuralNetwork, GenerationGeneticNN

def main():
    parser = argparse.ArgumentParser(prog="lab4py", description="4. lab vjezba iz kolegija uuui", epilog="Long Live The King")

    parser.add_argument("--train", required=True)
    parser.add_argument("--test", required=True)
    parser.add_argument("--nn", required=True)
    parser.add_argument("--popsize", type=int, required=True)
    parser.add_argument("--elitism", type=int, required=True)
    parser.add_argument("--p", type=float, required=True)
    parser.add_argument("--K", type=float, required=True)
    parser.add_argument("--iter", type=int, required=True)
    args = parser.parse_args()

    args = parser.parse_args()
    train_data = utils.load_data(args.train)
    test_data = utils.load_data(args.test)
    #print(train_data)
    #print(test_data)

    nn = NeuralNetwork(input_size = len(train_data.get("X")[0]), output_size = utils.broj_stupaca_po_elementu(train_data.get("y"))[0], config = args.nn)
    nn.foward_pass_all(train_data)

    input_size = len(train_data.get("X")[0])
    output_size = utils.broj_stupaca_po_elementu(train_data.get("y"))[0]
    config = args.nn
    popsize = args.popsize
    elitism = args.elitism
    mutation_probability = args.p
    gauss_std = args.K 
    num_of_iter = args.iter
    nn2 = GenerationGeneticNN(input_size, output_size, config, popsize, elitism, mutation_probability, gauss_std, num_of_iter)
    nn2.train(train_data)
    nn2.test(test_data)

if __name__ == "__main__":
    main()