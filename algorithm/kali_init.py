def int_to_bin_array(val, bits)
    return [(val  i) & 1 for i in reversed(range(bits))]

def kali_initialize_inputs(crossbar, A, B, N)
    
    Maps input A to row 0, columns 2 to N+2
    Maps input B to column 0, rows 1 to N+1
    
    a_bits = int_to_bin_array(A, N)
    b_bits = int_to_bin_array(B, N)

    # Map A → row 0, columns 2 to N+2
    for i, bit in enumerate(a_bits)
        crossbar.write(0, i + 2, bit)

    # Map B → column 0, rows 1 to N+1
    for i, bit in enumerate(b_bits)
        crossbar.write(i + 1, 0, bit)

    return a_bits, b_bits
