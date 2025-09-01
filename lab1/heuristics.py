import heapq
from collections import defaultdict

import utils


def find_shortes_paths(graph, goal):
    reversed_graph = defaultdict(list)
    minimal_prices = defaultdict(list)

    # dodajem sva stanja u revers_graph:
    for (state, transitions) in graph.items():
        reversed_graph[state]
        minimal_prices[state] = float("inf")
    
    minimal_prices[goal] = float(0.0)

    # punimo obrnuti graf
    for (state, transitions) in graph.items():
        for (next_state, price) in transitions:
            reversed_graph[next_state].append((state, price))
    
    #provođenje dijsktra algortima
    heap = []
    heapq.heappush(heap, (float(0.0), goal))

    while heap:
        (current_price, current_state) = heapq.heappop(heap)

        if current_price > minimal_prices[current_state]:
            continue

        for (neighbour, transition_price) in reversed_graph[current_state]:
            new_distance = current_price + transition_price

            if new_distance < minimal_prices[neighbour]:
                minimal_prices[neighbour] = new_distance
                heapq.heappush(heap, (new_distance, neighbour))

    return minimal_prices

# KOMENTAR:
    """
    Funkcija find_shortes_paths() - Pronalazi najkraće udaljenosti od svih stanja do ciljnog stanja `goal` korištenjem Dijkstrinog algoritma na obrnutom grafu.

    Složenost:
    1. Dijkstra na obrnutom grafu: O((V + E) log V)
    - V = broj stanja (čvorova)
    - E = broj prijelaza (bridova)
    2. Ukupno za G ciljnih stanja: O(G * (V + E) log V)

    Ukupna složenost provjere optimističnosti:
    - Pozivi find_shortes_paths(): O(G * (V + E) log V)
    - Izgradnja final_shortest: O(V * G)
    - Provjera heuristike: O(V)

    * Ukupno: O(G * (V + E) log V + V * G)

    Efikasnost u odnosu na naivne pristupe:
    - Floyd-Warshall (svi parovi): O(V³)    :(
    - Ovaj pristup: O(V² log V) za G ≈ V    :)
   """

def optimistic(prostor_stanja, h_path):
    if h_path:
        heuristic = utils.load_h(h_path)
    print("# HEURISTIC-OPTIMISTIC {}".format(h_path))
    
    # dodajem svako prihvatljivo stanje u shortes_paths kao kljuc
    shortes_paths = defaultdict(list)
    for goal in prostor_stanja["goal"]:
        shortes_paths[goal] = find_shortes_paths(prostor_stanja.get("transitions"), goal)

    # nademo najmanje udaljensoti od svih najmanjih udaljenosti:
    final_shortest = {state : (min(min_prices[state] for state_inside, min_prices in shortes_paths.items())) for state, _ in prostor_stanja.get("transitions").items()}

    sorted_keys = sorted(heuristic.keys())
    is_optimistic = True

    for state in sorted_keys:
        if heuristic[state] <= final_shortest[state]:
            print("[CONDITION]: [OK] h({}) <= h*: {} <= {}".format(state, heuristic[state], final_shortest[state]))
        else:
            print("[CONDITION]: [ERR] h({}) <= h*: {} <= {}".format(state, heuristic[state], final_shortest[state]))
            is_optimistic = False

    if is_optimistic:
        print("[CONCLUSION]: Heuristic is optimistic.")
    else:
        print("[CONCLUSION]: Heuristic is not optimistic.")

# KOMENTAR:
    """ 
        Prolazimo kroz svako stanje kojih ima V i onda po svakom njegovom susjedu,
        O (V * b), di je b faktor granjanja
        Vjerovatno je moglo i bolje ali i ovo je sasvim okej :)
    """

def consistent(prostor_stanja, h_path):
    if h_path:
        heuristic = utils.load_h(h_path)
    print("# HEURISTIC-CONSISTENT {}".format(h_path))

    graph = prostor_stanja.get("transitions")
    sorted_keys = sorted(graph.keys())
    is_consistent = True

    for state in sorted_keys:
        transitions = graph[state]
        h_state = heuristic[state]
        for next_state, price in transitions:
            if h_state <= heuristic[next_state] + price:
                print("[CONDITION]: [OK] h({}) <= h({}) + c: {} <= {} + {}".format(state, next_state, h_state, heuristic[next_state], price))
            else:
                print("[CONDITION]: [ERR] h({}) <= h({}) + c: {} <= {} + {}".format(state, next_state, h_state, heuristic[next_state], price))
                is_consistent = False

    if is_consistent:
        print("[CONCLUSION]: Heuristic is consistent.")
    else:
        print("[CONCLUSION]: Heuristic is not consistent.")
