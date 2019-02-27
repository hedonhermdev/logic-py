from gates import Connector, AND, OR, NOT, H, L


and1 = AND()
not1 = NOT()
or1 = OR()

and1.set_pin("A", H)
and1.set_pin("B", H)

and1.perform_logic()

c1 = Connector(and1.pins["OUT"], not1.pins["A"])
c1.connect()

not1.perform_logic()

Y = not1.get_output_signal()
print(Y.label)