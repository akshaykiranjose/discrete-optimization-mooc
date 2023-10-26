from copy import deepcopy
from collections import namedtuple
from time import time
import numpy as np

Item = namedtuple("Item", ['index', 'value', 'weight'])
Node = namedtuple("Node", ['value', 'room', 'esimtate', 'taken', 'nextitem'])

def estimate1(items, cap):
    return sum([i.value for i in items])

def estimate2(items, cap):
    est = 0
    for item in items:
        if cap >= item.weight:
            est += item.value
            cap -= item.weight
        else:
            est += item.value * cap / item.weight
            break
    return int(est)

def dfbb(items, room, estimate_fn = estimate2):
    start = time()

    best_value = 0
    best_taken = [0]*len(items)

    stack = [Node(0, room, estimate_fn(items, room), [0]*len(items), 0)]

    while stack:
        node = stack.pop()
        cur_idx = node.nextitem
        cur_val = node.value
        cur_est = node.esimtate
        cur_taken = node.taken
        cur_room = node.room
        

        if cur_val > best_value:
            best_value = cur_val
            best_taken = cur_taken

        #print(node, best_value)

        if cur_est > best_value and cur_idx < len(items):

            #not to take
            notake_taken = deepcopy(cur_taken)
            notake_taken[cur_idx] = 0
            stack.append(Node(cur_val, 
            cur_room, 
            cur_val + estimate_fn(items[cur_idx+1:], cur_room), 
            #cur_est - items[cur_idx].value,
            notake_taken,
            cur_idx + 1))

            if cur_room >= items[cur_idx].weight:
                # to take
                take_taken = deepcopy(cur_taken)
                take_taken[cur_idx] = 1
                stack.append(Node(cur_val + items[cur_idx].value, 
                cur_room - items[cur_idx].weight, 
                cur_est, 
                take_taken,
                cur_idx + 1))
            
        if int(time() - start) > 400:
            break
    
    return best_value, best_taken

def solve_it(input_data):
    lines = input_data.split('\n')
    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])
    items = []

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1])))
    
    items_sorted = sorted(items, key = lambda x: x.value/x.weight, reverse = True)
    sorted_idxs = np.argsort([i.index for i in items_sorted])
    
    #print(sorted_idxs)
    best_value, best_taken = dfbb(items_sorted, capacity, estimate2)

    value = best_value
    taken = list(np.array(best_taken)[sorted_idxs])#get it back in order

    # sanity_taken = 0
    # for boolean, item in zip(taken, items):
    #     sanity_taken += item.value * boolean
    #print(sanity_taken)

    output_data = str(value) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data


# def solve_it(input_data):
#     # Modify this code to run your optimization algorithm

#     # parse the input
#     lines = input_data.split('\n')

#     firstLine = lines[0].split()
#     item_count = int(firstLine[0])
#     capacity = int(firstLine[1])

#     items = []

#     for i in range(1, item_count+1):
#         line = lines[i]
#         parts = line.split()
#         items.append(Item(i-1, int(parts[0]), int(parts[1])))

#     # a trivial algorithm for filling the knapsack
#     # it takes items in-order until the knapsack is full
#     value = 0
#     weight = 0
#     taken = [0]*len(items)

#     for item in items:
#         if weight + item.weight <= capacity:
#             taken[item.index] = 1
#             value += item.value
#             weight += item.weight
    
#     # prepare the solution in the specified output format
#     output_data = str(value) + ' ' + str(0) + '\n'
#     output_data += ' '.join(map(str, taken))
#     return output_data


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')

