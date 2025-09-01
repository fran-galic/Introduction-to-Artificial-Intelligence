import random
import numpy as np

class NeuralNetwork:

    def __init__(self, input_size = 3, output_size = 1, config = "5s"):
        # mozda ce trebait pretvorti u numpy polja ili necemo korisitti uopce
        self.input_dim = input_size + 1
        self.output_dim = output_size
        self.hidden_layers_dim = []
        self.weights = []

        for n in config.split("s"):
            try:
                broj = int(n)
                self.hidden_layers_dim.append(broj)
            except ValueError:
                continue

        current_input_dim = self.input_dim
        for i in range(len(self.hidden_layers_dim)):
            dimenzija_izlaza = self.hidden_layers_dim[i]
            M = np.array([ np.random.normal(loc=0, scale=0.01, size=current_input_dim) for _ in range(dimenzija_izlaza)])
            self.weights.append(M)
            current_input_dim = dimenzija_izlaza + 1
        # zadnja matrica za zandji skrievni sloj i izlaz
        M_last = np.array([ np.random.normal(loc=0, scale=0.01, size=current_input_dim) for _ in range(self.output_dim)])
        self.weights.append(M_last)

        # for i, M in enumerate(self.weights):
            # print(f"{i}. Matrica")
            # print(M)
            # print()
    
    def _prijenosna_funkcija(self, x: np.ndarray):
        return 1 / (1 + np.exp(-x))
    
    def _foward_pass_single(self, input):
        input = np.array(input, dtype=float)
        ulaz = np.concatenate([input, [1.0]])
        for M in self.weights[:-1]:
            izlaz = self._prijenosna_funkcija(M @ ulaz)
            ulaz = np.concatenate([izlaz, [1]])
        # na zadnji ne primjenujemo prijenoasnu funkciju 
        izlaz = self.weights[-1] @ ulaz
        return izlaz
    
    def _MSE(self, y_real, y_obtained):
        y_real = np.array(y_real, dtype=float)
        y_obtained = np.array([
            yo[0] if isinstance(yo, (list, np.ndarray)) and len(yo) == 1 else float(yo)
            for yo in y_obtained
        ], dtype=float)
        return np.mean((y_real - y_obtained) ** 2)
    
    def foward_pass_all(self, data):
        # print("Vrtimo foward pass za sve primjere")
        X = data.get("X")
        y_original = data.get("y")
        y_obtained = np.full(len(y_original), None, dtype=object)
        for i, (x_row, y) in enumerate(zip(X, y_original)):
            # print(f"{i}. primjer: {x_row}")
            y_obtained[i] = self._foward_pass_single(x_row)
            # print(f"Ocekivani rezultat: {y}, Dobiveni rezultat: {y_obtained[i]}")
            # print()
        mse = self._MSE(y_original, y_obtained)
        # print()
        # print(f"Srednje kvadratno odstupanje za sve primjere iznosi: {mse}")
        return mse
    
    def get_weights(self):
        return [w.copy() for w in self.weights] 

    def set_weights(self, new_weights):
        if len(new_weights) != len(self.weights):
            raise ValueError("Broj slojeva se ne poklapa.")
        for i, (w_new, w_old) in enumerate(zip(new_weights, self.weights)):
            if w_new.shape != w_old.shape:
                raise ValueError(f"Težine sloja {i} ne odgovaraju po obliku.")
            self.weights[i] = np.array(w_new)

class GenerationGeneticNN:
    def __init__(self, input_size = 3, output_size = 1, config = "5s", popsize = 30, elitism = 3, 
                 mutation_probability = 0.05, gauss_std = 0.01, num_of_iter = 10000):
        self.input_size = input_size
        self.output_size = output_size
        self.config = config
        self.popsize = popsize
        self.elitism = elitism
        self.mutation_probability = mutation_probability
        self.gauss_std = gauss_std
        self.num_of_iter = num_of_iter
        self.best_network = None

    def train(self, data):
        current_population = [ NeuralNetwork(self.input_size, self.output_size, self.config) for _ in range(self.popsize)]
        for j in range(1, self.num_of_iter + 1):
            mse_and_index_array = []
            for i, jedinka in enumerate(current_population):
                mse_and_index_array.append((i ,jedinka.foward_pass_all(data)))
            mse_and_index_sorted = sorted(mse_and_index_array, key=lambda x: x[1])
            elitini_indeksi = [x[0] for x in mse_and_index_sorted[:self.elitism]]
            new_generation = [current_population[i] for i in elitini_indeksi]
            # dodamo i sve presotale krizanjem orginalnih roditleja:
            fitnessi = [x[1] for x in mse_and_index_array]
            for _ in range(self.popsize - self.elitism):
                p1 = self._roulette_selection(current_population, fitnessi)
                p2 = self._roulette_selection(current_population, fitnessi)
                child_weights = self._crossing(p1, p2)
                child_weights = self._mutate(child_weights)
                child = NeuralNetwork(self.input_size, self.output_size, self.config)
                child.set_weights(child_weights)
                new_generation.append(child)
            if j % 2000 == 0:
                print(f"[Train error @{j}]: {mse_and_index_sorted[0][1]}")
            current_population = new_generation
        self.best_network = current_population[elitini_indeksi[0]]
    
    def test(self, data):
        print(f"[Test error]: {self.best_network.foward_pass_all(data)}")


    def _roulette_selection(self, population, fitnessi, epsilon=1e-6):
        min_fitness = min(fitnessi)
        offset = abs(min_fitness) + epsilon
        adjusted_fitness = [f + offset for f in fitnessi]
        total = sum(adjusted_fitness)
        inverted = [1 / (f + epsilon) for f in fitnessi]
        total = sum(inverted)
        probabilities = [f / total for f in inverted]
        return random.choices(population, weights=probabilities, k=1)[0]

    def _crossing(self, p1 : NeuralNetwork, p2 : NeuralNetwork):
        w1 = p1.get_weights()
        w2 = p2.get_weights()
        new_weights = []
        for mat1, mat2 in zip(w1, w2):
            new_weights.append((mat1 + mat2) / 2)
            # moj pokusaj da popraivm:
            # alpha = np.random.uniform(0, 1)
            # new_weights.append(alpha * mat1 + (1 - alpha) * mat2)
        return new_weights

    
    def _mutate(self, child_weights):
        new_weights = []
        for M in child_weights:
            M_novo = M.copy()
            for i in range(M.shape[0]):
                for j in range(M.shape[1]):
                    if random.random() < self.mutation_probability:
                        M_novo[i, j] += np.random.normal(0, self.gauss_std)
            new_weights.append(M_novo)

        return new_weights