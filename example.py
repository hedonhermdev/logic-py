from gates import Connector, AND, OR, NOT, NAND, NOR, H, L


# Y =  ~(~(A + B) * (A * B))

A = H
B = L

# C = A (NOR) B
nor1 = NOR()
nor1.set_pin("A", A)
nor1.set_pin("B", B)
nor1.perform_logic()

C = nor1.pins["OUT"]


# D = A (AND) B
and1 = AND()
and1.set_pin("A", A)
and1.set_pin("B", B)
and1.perform_logic()

D = and1.pins["OUT"]

# Y = C (NAND) D
nand1 = NAND()

c1 = Connector(C, nand1.pins["A"])
c2 = Connector(D, nand1.pins["B"])
c1.connect()
c2.connect()

nand1.perform_logic()

Y = nand1.get_output_signal()

print(Y.label)
