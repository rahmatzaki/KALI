from simulator.crossbar import Crossbar
from simulator.partition import PartitionManager
from algorithm.kali_init import kali_initialize_inputs
from algorithm.partial_product import generate_partial_products
from algorithm.bit_shift import assign_bit_shifts
from algorithm.wallace_reduction import wallace_reduction
from algorithm.prefix_adder import prefix_addition

def kali_multiplication(A, B, N=4):
    """
    Perform KALI multiplication for given integers A and B.
    Default N=4 bits for quick testing (can set N=32, 64 later).
    """
    crossbar = Crossbar(rows=300, cols=300)  # adjust bigger if needed
    partitions = PartitionManager(crossbar, num_partitions=2 * N)

    # Step 1: Initialize inputs
    kali_initialize_inputs(crossbar, A, B, N)

    # Step 2: Generate partial products
    generate_partial_products(crossbar, N)

    # Step 3: Bit shifting
    assign_bit_shifts(crossbar, partitions, N)

    # Step 4: Wallace reduction
    wallace_reduction(crossbar, partitions)

    # Step 5: Prefix adder
    final_sum = prefix_addition(crossbar, partitions, N)

    return final_sum, crossbar

if __name__ == "__main__":
    # Example: Multiply 5 * 3
    A = 5
    B = 3
    N = 4  # You can change to 8, 16, 32, 64 for bigger tests

    result, crossbar = kali_multiplication(A, B, N)

    # Convert binary result back to integer
    result_bits = [result[i] for i in sorted(result.keys())]
    decimal_result = 0
    for idx, bit in enumerate(reversed(result_bits)):
        decimal_result += bit << idx

    print(f"A = {A}, B = {B}")
    print(f"KALI Multiplication Result = {decimal_result}")
    print(f"Expected = {A * B}")
    print(f"Latency = {crossbar.get_latency()} cycles")
    print(f"Energy = {crossbar.get_energy()} ops")
