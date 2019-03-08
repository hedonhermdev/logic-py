from circuit import Circuit
import components as comps

# Half adder is used to add two 1 bit binary numbers

adder = Circuit("MY CIRCUIT")

adder.add_input_pins('IN A', 'IN B')

adder.add_output_pins('CARRY', 'SUM')

adder.add_new_layer("Layer 1")

adder.add_new_gate(comps.EXOR("EXOR1"), "Layer 1", {'A': adder.input_pins['IN A'], 'B': adder.input_pins['IN B']})
adder.add_new_gate(comps.AND("AND1"), "Layer 1", {'A': adder.input_pins['IN A'], 'B': adder.input_pins['IN B']})

adder.new_output_connection("AND1", 'CARRY')
adder.new_output_connection("EXOR1", 'SUM')


adder.give_inputs({'IN A': comps.H, 'IN B': comps.H})

print(adder.get_output())

