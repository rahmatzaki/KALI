# kali_crossbar_simulator/simulator/crossbar.py

import numpy as np

class Crossbar:
    """
    Simulates a memristor crossbar array capable of performing NOR, NOT, and COPY operations.
    Each cell stores a binary bit (0 or 1).
    """

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.array = np.zeros((rows, cols), dtype=np.uint8)
        self.latency_counter = 0
        self.energy_counter = 0

    def reset(self):
        self.array.fill(0)
        self.latency_counter = 0
        self.energy_counter = 0

    def write(self, row, col, value):
        assert value in (0, 1)
        self.array[row, col] = value

    def read(self, row, col):
        return self.array[row, col]

    def NOT(self, src_row, dst_row, col_range):
        for col in col_range:
            self.array[dst_row, col] = 1 - self.array[src_row, col]
        self._update_cost(col_range)

    def NOR(self, row_a, row_b, dst_row, col_range):
        for col in col_range:
            a = self.array[row_a, col]
            b = self.array[row_b, col]
            self.array[dst_row, col] = int(not (a or b))
        self._update_cost(col_range)

    def COPY(self, src_row, dst_row, col_range):
        for col in col_range:
            self.array[dst_row, col] = self.array[src_row, col]
        self._update_cost(col_range)

    def _update_cost(self, col_range):
        ops = len(col_range)
        self.latency_counter += 1
        self.energy_counter += ops

    def get_state(self):
        return self.array.copy()

    def get_latency(self):
        return self.latency_counter

    def get_energy(self):
        return self.energy_counter


# kali_crossbar_simulator/simulator/partition.py

class PartitionManager:
    """
    Handles logical partitions within the crossbar.
    Each partition stores bits aligned by their binary significance (i+j).
    """
    def __init__(self, crossbar, num_partitions):
        self.crossbar = crossbar
        self.num_partitions = num_partitions
        self.partitions = {i: [] for i in range(num_partitions)}

    def assign(self, bit_row, bit_col, i, j):
        """
        Assign partial product a_i * b_j to partition i+j.
        """
        partition_id = i + j
        assert partition_id < self.num_partitions
        self.partitions[partition_id].append((bit_row, bit_col))

    def get_partition(self, partition_id):
        return self.partitions.get(partition_id, [])

    def get_all(self):
        return self.partitions

    def reset(self):
        self.partitions = {i: [] for i in range(self.num_partitions)}


# kali_crossbar_simulator/algorithm/kali_init.py

def int_to_bin_array(val, bits):
    return [(val >> i) & 1 for i in reversed(range(bits))]

def kali_initialize_inputs(crossbar, A, B, N):
    """
    Maps input A to row 0, columns 2 to N+2
    Maps input B to column 0, rows 1 to N+1
    """
    a_bits = int_to_bin_array(A, N)
    b_bits = int_to_bin_array(B, N)

    # Map A → row 0, columns 2 to N+2
    for i, bit in enumerate(a_bits):
        crossbar.write(0, i + 2, bit)

    # Map B → column 0, rows 1 to N+1
    for i, bit in enumerate(b_bits):
        crossbar.write(i + 1, 0, bit)

    return a_bits, b_bits


# kali_crossbar_simulator/algorithm/partial_product.py

def generate_partial_products(crossbar, N, offset=2):
    """
    Generates partial products a_i * b_j using NOR-based logic:
    a AND b = NOT(NOR(NOT a, NOT b))
    Inputs:
        - A bits at row 0, cols offset to offset+N
        - B bits at rows 1 to N, col 0
    Output:
        - Partial products stored in row i+1+j (or custom layout)
    """
    temp_row1 = crossbar.rows - 3
    temp_row2 = crossbar.rows - 2
    dst_start = crossbar.rows - N*N - 1  # just for example, adjust later

    for i in range(N):
        for j in range(N):
            a_col = offset + i
            b_row = 1 + j
            dst_row = dst_start + i * N + j

            # NOT a → temp_row1
            crossbar.NOT(0, temp_row1, [a_col])
            # NOT b → temp_row2
            crossbar.NOT(b_row, temp_row2, [0])
            # NOR(NOT a, NOT b) → dst
            crossbar.NOR(temp_row1, temp_row2, dst_row, [0])

    return dst_start


# kali_crossbar_simulator/algorithm/bit_shift.py

def assign_bit_shifts(partition_manager, N, dst_start_row):
    """
    After partial products are generated, assign each (i, j) partial product
    to the correct partition based on bit weight (i+j).
    """
    for i in range(N):
        for j in range(N):
            dst_row = dst_start_row + i * N + j
            bit_col = 0  # All results stored in column 0 after generation
            partition_manager.assign(dst_row, bit_col, i, j)

    return partition_manager.get_all()
