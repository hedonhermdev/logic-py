class Signal:
    def __init__(self, value, label):
        self.value = value
        self.label = label


H = Signal(1, "High")  # High
L = Signal(0, "Low")  # Low


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
        self.pins = {"OUT": self.out_pin}

    def logic(self):
        pass

    def get_output_signal(self):
        return self.out_pin.get_state()

    def perform_logic(self):
        if self.pins["A"].isSet:
            self.pins["OUT"].set_state(self.logic())
        else:
            raise Exception("Pin A has no input signal")


class UnaryGate(Gate):
    # Gate with single pin
    def __init__(self, label):
        Gate.__init__(self, label)
        self.pin1 = Pin("A")
        self.pins.update({"A": self.pin1})

    def set_pin_state(self, label, signal):
        try:
            self.pins[label].set_state(signal)
        except:
            raise Exception("%s Gate has only one pin: A" % self.label)


class BinaryGate(Gate):
    # Gate with two pins
    def __init__(self, label):
        Gate.__init__(self, label)
        self.pin1 = Pin("A")
        self.pin2 = Pin("B")
        self.pins.update({"A": self.pin1})
        self.pins.update({"B": self.pin2})

    def set_pin(self, label, signal):
        try:
            self.pins[label].set_state(signal)
        except:
            raise Exception("%s Gate has only two pins: A and B" % self.label)


# ---
# Connector (wire to connect two pins).
class Connector:
    def __init__(self, from_pin, to_pin):
        self.from_pin = from_pin
        self.to_pin = to_pin

    def connect(self):
        if self.from_pin.isSet:
            sig = self.from_pin.get_state()
            self.to_pin.set_state(sig)
        else:
            raise Exception("State of from-pin is not set. ")


# ---
# The Gates
class NOT(UnaryGate):
    def __init__(self):
        UnaryGate.__init__(self, "NOT")

    def logic(self):
        if self.pins["A"].get_state() == H:
            return L
        else:
            return H


class AND(BinaryGate):
    def __init__(self):
        BinaryGate.__init__(self, "AND")

    def logic(self):
        if self.pins["A"].get_state() == H and self.pins["B"].get_state() == H:
            return H
        else:
            return L


class OR(BinaryGate):
    def __init__(self):
        BinaryGate.__init__(self, "OR")

    def logic(self):
        if self.pins["A"].get_state() == H or self.pins["B"].get_state() == H:
            return H
        else:
            return L


class EXOR(BinaryGate):
    def __init__(self):
        BinaryGate.__init__(self, "EX-OR")

    def logic(self):
        if self.pins["A"].get_state() == H or self.pins["B"].get_state() == H:
            if not (self.pins["A"].get_state() == H and self.pins["B"].get_state() == H):
                return H
        else:
            return L


class NAND(BinaryGate):
    def __init__(self):
        BinaryGate.__init__(self, "NAND")

    def logic(self):
        # NAND is NOT gate connected to output of AND gate
        a = AND()
        n = NOT()
        a.set_pin("A", self.pins["A"].get_state())
        a.set_pin("B", self.pins["B"].get_state())
        a.perform_logic()
        print(a.get_output_signal().label)
        c = Connector(a.pins["OUT"], n.pins["A"])
        c.connect()
        n.perform_logic()
        return n.get_output_signal()


class NOR(BinaryGate):
    def __init__(self):
        BinaryGate.__init__(self, "NOR")

    def logic(self):
        # NOR is NOT gate connected to output of OR gate
        o = OR()
        n = NOT()
        o.set_pin("A", self.pins["A"].get_state())
        o.set_pin("B", self.pins["B"].get_state())
        o.perform_logic()
        c = Connector(o.pins["OUT"], n.pins["A"])
        c.connect()
        n.perform_logic()


class EXNOR(BinaryGate):
    def __init__(self):
        BinaryGate.__init__(self, "EX-NOR")

    def logic(self):
        eo = EXOR()
        n = NOT()
        eo.set_pin("A", self.pins["A"].get_state())
        eo.set_pin("B", self.pins["B"].get_state())
        eo.perform_logic()
        c = Connector(eo.pins["OUT"], n.pins["A"])
        c.connect()
        n.perform_logic()