# Two input multiplexer.
# Y = [ A (AND) [(NOT)X] ] (OR) [ B (AND) X ]

from components import *
from circuit import Circuit

multiplexer = Circuit('MULTIPLEXER')

# SETUP----------------------------

# INPUTS
multiplexer.add_input_pins('X', 'A', 'B')

# OUTPUT
multiplexer.add_output_pins('Y')

# First Layer
multiplexer.add_new_layer('Layer 1')
multiplexer.add_new_gate(NOT('NOT 1'), 'Layer 1', {'A': multiplexer.input_pins['X']})

# Second Layer
multiplexer.add_new_layer('Layer 2')
multiplexer.add_new_gate(AND('AND 1'), 'Layer 2', {'A': multiplexer.input_pins['A'], 'B': multiplexer.gates['NOT 1'].pins['OUT']})
multiplexer.add_new_gate(AND('AND 2'), 'Layer 2', {'A': multiplexer.input_pins['B'], 'B': multiplexer.input_pins['X']})

# Third Layer
multiplexer.add_new_layer('Layer 3')
multiplexer.add_new_gate(OR('OR 1'), 'Layer 3', {'A': multiplexer.gates['AND 1'].pins['OUT'], 'B': multiplexer.gates['AND 2'].pins['OUT']})

# Output Connection
multiplexer.new_output_connection('OR 1', 'Y')


# EXECUTION------------------------
print("MULTIPLEXER")
print("EQUATION: Y = [ A (AND) [(NOT)X] ] (OR) [ B (AND) X ]")

# Inputs
print("INPUTS: ")
a = input("A > ")
b = input("B > ")
x = input("X > ")

multiplexer.give_inputs({'A': a, 'B': b, 'X': x})

Y = multiplexer.get_output()



