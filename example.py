from gates import Connector, AND, OR, NOT, NAND, NOR, H, L


# Y =  ~(~(A + B) * (A * B))

A = H
B = H

# C = A (NOR) B
nor1 = NOR()
nor1.set_pin("A", A)
nor1.set_pin("B", B)
nor1.perform_logic()

C = nor1.get_output_signal()


# D = A (AND) B
and1 = AND()
and1.set_pin("A", A)
and1.set_pin("B", B)
and1.perform_logic()

D = and1.get_output_signal()

# Y = C (NAND) D
nand1 = NAND()
nand1.set_pin("A", C)
nand1.set_pin("B", D)
nand1.perform_logic()

Y = nand1.get_output_signal()

print(Y.label)
