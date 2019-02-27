class Signal:
    def __init__(self, value, label):
        self.value = value
        self.label = label
H = Signal(1, "High") # High
L = Signal(0, "Low") # Low


# ---
# Pins for gates
class Pin:
    # Class for pin
    def __init__(self, label):
        self.label = label
        self.state = None
        self.isSet = False

    def set_state(self, signal):
        # Set state of pin as H or L
        self.isSet = True
        self.state = signal

    def get_state(self):
        # Returns a signal from the pin
        if self.isSet:
            return self.state
        else:
            raise Exception("Pin is not set.")


# ---
# Base classes for gates
class Gate:
    # Base gate class
    def __init__(self, label):
        self.label = label
        self.out_pin = Pin("OUT")
        self.pins = []

    def logic(self):
        pass

    def get_output_signal(self):
        return self.out_pin.get_state()

    def perform_logic(self):
        if self.pin1.isSet:
            self.out_pin.set_state(self.logic())
        else:
            raise Exception("Pin A has no input signal")


class UnaryGate(Gate):
    # Gate with single pin
    def __init__(self, label):
        Gate.__init__(self, label)
        self.pin1 = Pin("A")
        self.pins.append(self.pin1)

    def set_pin(self, label, signal):
        if label == "A":
            self.pin1.set_state(signal)
        else:
            raise Exception("Gate has only one pin: A")


class BinaryGate(Gate):
    # Gate with two pins
    def __init__(self, label):
        Gate.__init__(self, label)
        self.pin1 = Pin("A")
        self.pin2 = Pin("B")
        self.pins.append(self.pin1)
        self.pins.append(self.pin2)

    def set_pin(self, label, signal):
        if label == "A":
            self.pin1.set_state(signal)
        elif label == "B":
            self.pin2.set_state(signal)
        else:
            raise Exception("Gate has only two pins: A and B")


# ---
# Connector (wire to connect two pins).
class Connector:
    def __init__(self, from_pin, to_pin):
        self.from_pin = from_pin
        self.to_pin = to_pin

    def connect(self):
        if self.from_pin.isSet:
            sig = self.from_pin.get_state()
            self.pin2.set_state(sig)
        else:
            raise Exception("State of from-pin is not set. ")


# ---
# The Gates
class NOT(UnaryGate):
    def __init__(self):
        UnaryGate.__init__(self, "NOT")

    def logic(self):
        if self.pin1.get_state() == H:
            return L
        else:
            return H


class AND(BinaryGate):
    def __init__(self):
        BinaryGate.__init__(self, "AND")

    def logic(self):
        if self.pin1.get_state() == H and self.pin2.get_state() == H:
            return H
        else:
            return L


class OR(BinaryGate):
    def __init__(self):
        BinaryGate.__init__(self, "OR")

    def logic(self):
        if self.pin1.get_state() == H or self.pin2.get_state() == H:
            return H
        else:
            return L


