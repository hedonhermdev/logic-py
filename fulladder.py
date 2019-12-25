from components import *
from circuit import Circuit

# --------------------------------------------------------------
# SET UP
fulladder = Circuit('FULL ADDER')

fulladder.add_input_pins('A', 'B', 'C-IN')
A = fulladder.input_pins['A']
B = fulladder.input_pins['B']
C = fulladder.input_pins['C-IN']

# S = C-IN (EXOR) [ A (EXOR) B]
# C-OUT = [A (AND) B] (OR) [ C-IN (AND) [A (EXOR) B] ]
fulladder.add_output_pins('S', 'C-OUT')

# Full adder has 4 layers.
fulladder.add_new_layer('Layer 1')
fulladder.add_new_layer('Layer 2')
fulladder.add_new_layer('Layer 3')
fulladder.add_new_layer('Layer 4')

fulladder.add_new_gate(EXOR('EXOR 1'), 'Layer 1', {'A': A, 'B': B})

fulladder.add_new_gate(EXOR('EXOR 2'), 'Layer 2', {'A': fulladder.gates['EXOR 1'].pins['OUT'], 'B': C})

fulladder.new_output_connection('EXOR 2', 'S')

fulladder.add_new_gate(AND('AND 1'), 'Layer 3', {'A': C, 'B': fulladder.gates['EXOR 1'].pins['OUT']})

fulladder.add_new_gate(AND('AND 2'), 'Layer 3', {'A': A, 'B': B})

fulladder.add_new_gate(OR('OR 1'), 'Layer 4', {'A': fulladder.gates['AND 1'].pins['OUT'], 'B': fulladder.gates['AND 2'].pins['OUT']})

fulladder.new_output_connection('OR 1', 'C-OUT')


# ------------------------------------------------------------
# Execution
print("FULL ADDER")
print("EQUATION: S = (A XOR B XOR Cin), Cout = [(A AND B) OR (B AND Cin) OR (Cin AND A)]")
print("INPUTS:")
a = input("A > ")
b = input("B > ")
c = input("Cin > ")

fulladder.give_inputs({'A': a, 'B': b, 'C-IN': c})

OUT = fulladder.get_output()

[print("%s : %s" % (x, y)) for x, y in zip(OUT.keys(), OUT.values())]
