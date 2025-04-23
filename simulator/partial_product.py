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
