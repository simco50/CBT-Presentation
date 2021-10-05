import numpy as np
import Libraries.Utilities as Utils

def leb_triangle():
    return np.array([
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0],
        [1.0, 0.0, 0.0]
    ])

def identity():
    return np.array([
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0]
    ])

def split_matrix(bit):
    b = float(bit)
    c = 1.0 - bit
    return np.array([
        [ c, b, 0.0 ],
        [ 0.5, 0.0, 0.5 ],
        [ 0.0, c, b ]
    ])

def square_matrix(bit):
    b = float(bit)
    c = 1.0 - bit
    return np.array([
        [ c, 0.0, b ],
        [ b, c, b ],
        [ b, 0.0, c ]        
    ])

def winding_matrix(bit):
    b = bit
    c = 1.0 - b
    return np.array([
        [ c, 0.0, b ],
        [ 0.0, 1.0, 0.0 ],
        [ b, 0.0, c ]        
    ])

def get_bit(value, bit):
    return (value >> bit) & 1

def get_matrix(heap_index):
    d = Utils.most_signficant_bit(heap_index)
    m = identity()
    bit_index = d - 1
    while bit_index >= 0:
        bit = get_bit(heap_index, bit_index)
        split_m = split_matrix(bit)
        m = np.matmul(split_m, m)
        bit_index = bit_index - 1
    return np.matmul(winding_matrix(d & 1), m)

def get_vertices(heap_index):
    m = leb_triangle()
    m = np.matmul(get_matrix(heap_index), m)
    return m

def transform_vertices(matrix, scale=6):
    m = []
    for i, row in enumerate(matrix):
        m.append([])
        for j, element in enumerate(row):
            m[i].append((matrix[i][j] - 0.5) * scale)
    return m

def get_neighbors(heap_index):
    depth = Utils.most_signficant_bit(heap_index)
    n = [0, 0, 0, 1]

    bit_id = depth - 1
    while bit_id >= 0:
        n1 = n[0]
        n2 = n[1]
        n3 = n[2]
        n4 = n[3]
        b2 = 0 if n2 == 0 else 1
        b3 = 0 if n3 == 0 else 1
        if get_bit(heap_index, bit_id) is 0:
            n[0] = (n4 << 1) | 1
            n[1] = (n3 << 1) | b3
            n[2] = (n2 << 1) | b2
            n[3] = (n4 << 1)
        else:
            n[0] = (n3 << 1)
            n[1] = (n4 << 1)
            n[2] = (n1 << 1)
            n[3] = (n4 << 1) | 1

        bit_id -= 1
    return n