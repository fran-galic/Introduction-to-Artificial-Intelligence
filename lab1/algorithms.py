import heapq
from collections import deque

import utils


def bfs(prostor_stanja):
    general_search(type="bfs", prostor_stanja=prostor_stanja)
    
def ucs(prostor_stanja):
    general_search(type="ucs", prostor_stanja=prostor_stanja)

def astar(prostor_stanja, h_path):
    general_search(type="astar", prostor_stanja=prostor_stanja, h_path=h_path)


def general_search(type, prostor_stanja, h_path = None):
    if type == "astar" and h_path:
        heuristic = utils.load_h(h_path)
        print("# A-STAR {}".format(h_path))
    elif type == "ucs":
        print("# UCS")
    elif type == "bfs":
        print("# BFS")
    else: 
        ValueError("Nevažeći tip pretrage. Dozvoljene vrijednosti su 'astar', 'bfs' i 'ucs'.")


    # provođenje algoritma
    closed = set()
    open = []

    directions = {}
    cost_so_far = {}
    solution_found = False
    solution_state = None

    start = prostor_stanja.get("begin")
    cost_so_far[start] = 0
    heapq.heappush(open, (0 + (heuristic[start] if type == "astar" else 0), start, (start, 0)))

    while open:
        _, _, (current_state, current_accumulated) = heapq.heappop(open)

        if current_state in closed:
            continue

        closed.add(current_state)

        if current_state in prostor_stanja["goal"]:
            solution_found = True
            solution_state = current_state
            break

        next_states = prostor_stanja["transitions"].get(current_state, [])
        for (next_state, transition_cost) in next_states:
            used_cost = 1 if type == "bfs" else transition_cost
            new_cost = current_accumulated + used_cost

            if next_state not in cost_so_far or new_cost < cost_so_far.get(next_state, float('inf')):
                cost_so_far[next_state] = new_cost
                directions[next_state] = current_state
                heapq.heappush(open, (new_cost + (heuristic[next_state] if type == "astar" else 0), next_state, (next_state, new_cost)))

    # ispis
    if not solution_found:
        print("[FOUND_SOLUTION]: no")
        return
    
    # inače:
    print("[FOUND_SOLUTION]: yes")
    print("[STATES_VISITED]: {}".format(len(closed)))

    path_length = 0
    path_current_state = solution_state
    stack = deque()
    while path_current_state:
        path_length += 1
        stack.append(path_current_state)
        path_current_state = directions.get(path_current_state)
            
        
    print("[PATH_LENGTH]: {}".format(path_length))
    print("[TOTAL_COST]: {:.1f}".format(cost_so_far[solution_state]))
    stack.reverse()
    path_string = ""
    for index, state in enumerate(stack):
        path_string += state
        if index < len(stack) - 1:
            path_string += " => "
    print("[PATH]: {}".format(path_string))




