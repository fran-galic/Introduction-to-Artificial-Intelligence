import utils
import math
from collections import Counter

class ID3:
    def __init__(self, *args):
        if args:
            self.max_depth = args[0]
        else:
            self.max_depth = None
        self.root = _Node("None")
    
    def fit(self, data, max_depth= None):
        # utils.print_data(data)
        self._id3(data.get("X"), data.get("y"), data.get("y"), data.get("feature_names"), data.get("target_name"), self.root, max_depth)
        print(self.root)

    def predict(self, data):
        # utils.print_data(data)
        print()
        print("[PREDICTIONS]:", end="")
        results = []
        X = data.get("X")
        golden_marks = data.get("y")
        feature_names = data.get("feature_names")
        for row in X:
            result = self._predict_single(row, feature_names, self.root)
            print(f" {result}", end="")
            results.append(result)
        return results, golden_marks 

    def _predict_single(self, row, feature_names, current_node):
        while True:
            if current_node.is_leaf:
                return current_node.value
            else:
                current_feature = current_node.value
                f_index = feature_names.index(current_feature)
                feature_value = row[f_index]

            if feature_value in current_node.feature_value_to_children:
                next_node_index = current_node.feature_value_to_children.index(feature_value)
                current_node = current_node.children[next_node_index]
            else:
                return current_node.most_common_goal_value

    def _calc_entropy(self, y):
        counter = Counter(y)
        total = len(y)
        entropy = 0
        for count in counter.values():
            p = count / total
            if p > 0:
                entropy -= p * math.log2(p)
        return entropy
    
    def _get_unique_values(self, lst):
        seen = set()
        result = []
        for item in lst:
            if item not in seen:
                seen.add(item)
                result.append(item)
        return result

    def _id3(self, X, y, y_parrent, feature_names, target_name, current_node, max_depth):
        if len(y) == 0:
            current_node.is_leaf = True
            current_node.value = max(set(y_parrent), key=y_parrent.count)
            return
    
        if max_depth == 0:
            # akoje max_depth nula, nademo ciljnu oznaku koja je najsece zastupljena i jos prva abaecedno, znaci najmanja
            current_node.is_leaf = True
            counts_y = Counter(y)
            max_count = max(counts_y.values())
            najcesce_vrijednosti = [k for k, v in counts_y.items() if v == max_count]
            current_node.value = min(najcesce_vrijednosti) 
            return
        
        potencial_value = max(set(y), key=y.count) 
        # provjera dali je Matrica X prazna ili su sve oznake grupirane na jendoj vrijendosti:
        # gledmao dlai su sve unutrasnje liste prazne i da vanjska sadrzi barem neke elmente, da bi uopce bilo 2D polje
        if (all(len(unutarnja) == 0 for unutarnja in X) and len(X) > 0) or all(v == potencial_value for v in y):
            current_node.is_leaf = True
            current_node.value = potencial_value
            return 
        
        # Izračunaj max informacijsku dobit:
        initial_entropy = self._calc_entropy(y)
        max_IG = 0
        best_feature = None
        for feature in feature_names:
            f_IG = initial_entropy
            feature_index = feature_names.index(feature)
            column_values = [row[feature_index] for row in X]
            unique_values = self._get_unique_values(column_values)
            for u_value in unique_values:
                matching_indices = [i for i, row in enumerate(X) if row[feature_index] == u_value]
                new_y = [y[i] for i in matching_indices]
                f_IG -= (len(new_y)/len(y)) * self._calc_entropy(new_y)
            # jednom kada se izracuna IG za taj feature:
            if best_feature is None or f_IG > max_IG or (f_IG == max_IG and feature < best_feature):
                max_IG = f_IG
                best_feature = feature

        current_node.value = best_feature
        # nadi mi najsecu ciljnu vrijednost za svaki slucaj:
        counts_y = Counter(y)
        max_count = max(counts_y.values())
        najcesce_vrijednosti = [k for k, v in counts_y.items() if v == max_count]
        current_node.most_common_goal_value = min(najcesce_vrijednosti)

        max_feature_index = feature_names.index(best_feature)
        column_values = [row[max_feature_index] for row in X]
        unique_values = self._get_unique_values(column_values)

        for feature_value in unique_values:
            new_node = _Node("None")
            current_node.children.append(new_node)
            current_node.feature_value_to_children.append(feature_value)

            matching_indices = [i for i, row in enumerate(X) if row[max_feature_index] == feature_value]

            new_X = [
                [el for j, el in enumerate(row) if j != max_feature_index]
                for i, row in enumerate(X) if i in matching_indices
            ]
            new_y = [y[i] for i in matching_indices]
            new_feature_names = [f for i, f in enumerate(feature_names) if i != max_feature_index]

            if max_depth:
                self._id3(new_X, new_y, y, new_feature_names, target_name, new_node, max_depth - 1)
            else:
                self._id3(new_X, new_y, y, new_feature_names, target_name, new_node, None)

class _Node:
    def __init__(self, value, is_leaf=False):
        self.value = value 
        self.is_leaf = is_leaf
        self.children = []  
        self.feature_value_to_children = []
        # ima samo smisla ako je rijec ounutarnjem cvoru, a ne listu, i korsitmo ga kod predikcije
        self.most_common_goal_value = None

    def add_child(self, child_node, feature_value):
        self.children.append(child_node)
        self.feature_value_to_children.append(feature_value)

    def __repr__(self):
        lines = []
        self._build_repr(lines, path=[], level=1)
        return "\n[BRANCHES]:\n" + "\n".join(lines)

    def _build_repr(self, lines, path, level):
        if self.is_leaf:
            full_path = " ".join(path) + f" {self.value}"
            lines.append(full_path)
        else:
            for i, child in enumerate(self.children):
                feature_value = self.feature_value_to_children[i]
                part = f"{level}:{self.value}={feature_value}"
                child._build_repr(lines, path + [part], level + 1)
