#---
# Signal
class Signal:
    def __init__(self, value, label):
        self.value = value
        self.label = label

    def __repr__(self):
        return self.label[0]


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
        self.isConnected = False
        self.connected_via = []

    def __repr__(self):
        return "PIN: " + self.label

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
# Connector (wire to connect two pins).
class Connector:
    def __init__(self, from_pin, to_pin):
        self.from_pin = from_pin
        self.to_pin = to_pin
        self.from_pin.isConnected = True
        self.to_pin.isConnected = True
        self.to_pin.connected_via.append(self)
        self.from_pin.connected_via.append(self)

    def transfer_signal(self):
        if self.from_pin.isSet:
            sig = self.from_pin.get_state()
            self.to_pin.set_state(sig)

        else:
            raise Exception("State of from-pin is not set. ")


# ---
# Base classes for gates
class Gate:
    # Base gate class
    def __init__(self, label, name):
        self.label = label
        self.name = name
        self.pins = {"OUT": Pin("OUT")}

    def __repr__(self):
        return self.name

    def logic(self):
        pass

    def get_output_signal(self):
        return self.out_pin.get_state()

    def perform(self):
        pass


class UnaryGate(Gate):
    # Gate with single pin
    def __init__(self, label, name):
        Gate.__init__(self, label, name)
        self.pin1 = Pin("A")
        self.pins.update({"A": self.pin1})

    def set_pin_state(self, label, signal):
        try:
            self.pins[label].set_state(signal)
        except:
            raise Exception("%s Gate has only one pin: A" % self.label)

    def perform(self):
        self.pins['A'].connected_via[0].transfer_signal()
        out = self.logic()
        self.pins['OUT'].set_state(out)


class BinaryGate(Gate):
    # Gate with two pins
    def __init__(self, label, name):
        Gate.__init__(self, label, name)
        self.pin1 = Pin("A")
        self.pin2 = Pin("B")
        self.pins.update({"A": self.pin1})
        self.pins.update({"B": self.pin2})

    def set_pin(self, label, signal):
        try:
            self.pins[label].set_state(signal)
        except:
            raise Exception("%s Gate has only two pins: A and B" % self.label)

    def perform(self):
        self.pins['A'].connected_via[0].transfer_signal()
        self.pins['B'].connected_via[0].transfer_signal()
        out = self.logic()
        self.pins['OUT'].set_state(out)

# ---
# Buffer
class Buffer:
    def __init__(self, label):
        self.label = label
        self.name = "BUFFER"
        self.in_pin = Pin("IN")
        self.out_pin = Pin("OUT")
        self.pins = {'IN': self.in_pin, 'OUT': self.out_pin}

    def perform(self):
        self.out_pin.set_state(self.in_pin.get_state())

    def __repr__(self):
        return self.name


# ---
# The Gates
class NOT(UnaryGate):
    def __init__(self, label):
        UnaryGate.__init__(self, label, "NOT GATE")

    def logic(self):
        if self.pins["A"].get_state() == H:
            return L
        else:
            return H


class AND(BinaryGate):
    def __init__(self, label):
        BinaryGate.__init__(self, label, "AND GATE")

    def logic(self):
        if self.pins["A"].get_state() == H and self.pins["B"].get_state() == H:
            return H
        else:
            return L


class OR(BinaryGate):
    def __init__(self, label):
        BinaryGate.__init__(self, label, "OR GATE")

    def logic(self):
        if self.pins["A"].get_state() == H or self.pins["B"].get_state() == H:
            return H
        else:
            return L


class EXOR(BinaryGate):
    def __init__(self, label):
        BinaryGate.__init__(self, label, "EXOR GATE")

    def logic(self):
        if self.pins["A"].get_state() == H or self.pins["B"].get_state() == H:
            if not (self.pins["A"].get_state() == H and self.pins["B"].get_state() == H):
                return H
            else:
                return L
        else:
            return L


class NAND(BinaryGate):
    def __init__(self, label):
        BinaryGate.__init__(self, label, "NAND GATE")

    def logic(self):
        # NAND is NOT gate connected to output of AND gate
        a = AND('')
        n = NOT('')
        a.set_pin("A", self.pins["A"].get_state())
        a.set_pin("B", self.pins["B"].get_state())
        a.perform()
        c = Connector(a.pins["OUT"], n.pins["A"])
        c.transfer_signal()
        n.perform()
        return n.get_output_signal()


class NOR(BinaryGate):
    def __init__(self, label):
        BinaryGate.__init__(self, label, "NOR GATE")

    def logic(self):
        # NOR is NOT gate connected to output of OR gate
        o = OR()
        n = NOT()
        o.set_pin("A", self.pins["A"].get_state())
        o.set_pin("B", self.pins["B"].get_state())
        o.perform()
        c = Connector(o.pins["OUT"], n.pins["A"])
        c.transfer_signal()
        n.perform()


class EXNOR(BinaryGate):
    def __init__(self, label):
        BinaryGate.__init__(self, label, "EXNOR GATE")

    def logic(self):
        eo = EXOR('')
        n = NOT('')
        eo.set_pin("A", self.pins["A"].get_state())
        eo.set_pin("B", self.pins["B"].get_state())
        eo.perform()
        c = Connector(eo.pins["OUT"], n.pins["A"])
        c.transfer_signal()
        n.perform()
