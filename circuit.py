import components as comps


class Layer:
    def __init__(self, label):
        self.label = label
        self.gates = {}
        self.in_connectors = []

    def __repr__(self):
        return "LAYER: " + self.label

    def add_gate(self, gate):
        self.gates.update({gate.label: gate})


class Circuit:
    def __init__(self, label="UNNAMED CIRCUIT"):
        self.label = label
        self.input_pins = {}
        self.output_pins = {}
        self.layers = {}
        self.gates = {}
        self.output_connectors = []

    def __repr__(self):
        return self.label

    def add_input_pins(self, *labels):
        for label in labels:
            self.input_pins.update({label: comps.Pin(label)})

    def add_output_pins(self, *labels):
        for label in labels:
            self.output_pins.update({label: comps.Pin(label)})

    def give_inputs(self, inputs_dict):
        for pin in inputs_dict:
            self.input_pins[pin].set_state(inputs_dict[pin])

    def add_new_layer(self, label):
        layer = Layer(label)
        self.layers.update({layer.label: layer})

    def add_new_gate(self, gate, layer, inputs):
        self.layers[layer].add_gate(gate)
        self.gates.update({gate.label: gate})
        for inp in inputs:
            c = comps.Connector(inputs[inp], gate.pins[inp])

    def new_output_connection(self, gate_name, pin_name):
        c = comps.Connector(self.gates[gate_name].pins['OUT'], self.output_pins[pin_name])
        self.output_connectors.append(c)

    def execute(self):
        for layer in self.layers.values():
            for gate in layer.gates.values():
                gate.perform()

        for connector in self.output_connectors:
            connector.transfer_signal()

    def get_output(self):
        self.execute()
        return {pin.label: pin.get_state() for pin in self.output_pins.values()}


if __name__ == '__main__':

    circ = Circuit("MY CIRCUIT")

    A = comps.Pin("A")
    B = comps.Pin("B")
    circ.add_input_pins(A, B)
    S = comps.Pin("SUM")
    C = comps.Pin("CARRY")
    circ.add_output_pins(S, C)

    circ.add_new_layer("Layer 1")

    circ.add_new_gate(comps.AND("GATE 1"), "Layer 1", {"A": A, "B": B})
    circ.add_new_gate(comps.EXOR("GATE 2"), "Layer 1", {"A": A, "B": B})

    circ.new_output_connection("GATE 1", 'SUM')
    circ.new_output_connection("GATE 2", 'CARRY')
    circ.give_inputs({'A': comps.H, 'B': comps.L})
    print(circ.execute())
