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
