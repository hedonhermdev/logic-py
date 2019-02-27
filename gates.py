class Signal:
    def __init__(self, value):
        self.value = value

H = Signal(1) # High
L = Signal(0) # Low


class Pin:
    # Class for pin
    def __init__(self, label):
        self.label = label
        self.state = None
        self.isSet = False

    def set_state(self, signal):
        # Set state of pin as H or L
        self.isSet = True
        self.state = signal.value

    def get_state_signal(self):
        # Returns a signal from the pin
        if self.isSet:
            return Signal(self.state)
        else:
            raise Exception("Pin is not set.")


class Gate:
    # Base gate class
    def __init__(self, label):
        self.label = label
        self.out_pin = Pin("OUT")
        self.pins = []

    def logic(self):
        pass

    def get_output_signal(self):
        self.logic()
        return self.out_pin.get_state_signal()


class UnaryGate(Gate):
    # Gate with single pin
    def __init__(self, label):
        Gate.__init__(label)
        self.p1 = Pin("A")
        self.pins.append(self.p1)

    def set_pin(self, label):
        if label == "A":
            self.set_pin()

class BinaryGate(Gate):
    # Gate with two pins
    def __init__(self, label):
        Gate.__init__(self, label)
        self.p1 = Pin("A")
        self.p2 = Pin("B")



