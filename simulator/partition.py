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
