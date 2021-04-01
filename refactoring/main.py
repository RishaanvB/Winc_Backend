__winc_id__ = "9920545368b24a06babf1b57cee44171"
__human_name__ = "refactoring"

alice_name = "Alice Aliceville"
alice_profession = "electrician"
bob_name = "Bob Bobsville"
bob_profession = "painter"
craig_name = "Craig Craigsville"
craig_profession = "plumber"

alfred_name = "Alfred Alfredson"
alfred_address = "Alfredslane 123"
alfred_needs = ["painter", "plumber"]
bert_name = "Bert Bertson"
bert_address = "Bertslane 231"
bert_needs = ["plumber"]
candice_name = "Clyde Clydeson"
candice_address = "Clydeslane 312"
candice_needs = ["electrician", "painter"]

alfred_contracts = []
for need in alfred_needs:
    if need == alice_profession:
        alfred_contracts.append(alice_name)
    elif need == bob_profession:
        alfred_contracts.append(bob_name)
    elif need == craig_profession:
        alfred_contracts.append(craig_name)

bert_contracts = []
for need in bert_needs:
    if need == alice_profession:
        bert_contracts.append(alice_name)
    elif need == bob_profession:
        bert_contracts.append(bob_name)
    elif need == craig_profession:
        bert_contracts.append(craig_name)

candice_contracts = []
for need in candice_needs:
    if need == alice_profession:
        candice_contracts.append(alice_name)
    elif need == bob_profession:
        candice_contracts.append(bob_name)
    elif need == craig_profession:
        candice_contracts.append(craig_name)

print("Alfred's contracts:", alfred_contracts)
print("Bert's contracts:", bert_contracts)
print("Candice's contracts:", candice_contracts)
print("")


class Homeowner:
    def __init__(self, name, address, needs):
        self.name = name
        self.needs = needs
        self.address = address
        self.contracts = []

    def __repr__(self):
        return f"Hi! I am {self.name.title()} with a need for {self.needs}. I live at {self.address}"

    def add_specialist(self, specialist):
        self.contracts.append(specialist)


class Specialist:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"{self.name.title()}"


class Electrician(Specialist):
    pass


class Painter(Specialist):
    pass


class Plumber(Specialist):
    pass


alfred = Homeowner(alfred_name, alfred_address, [Painter, Plumber])
bert = Homeowner(bert_name, bert_address, [Plumber])
candice = Homeowner(candice_name, candice_address, [Electrician, Painter])


alice = Electrician(alice_name)
bob = Electrician(bob_name)
craig = Electrician(craig_name)


homeowners = [alfred, bert, candice]
specialist = {
    Electrician: Electrician("Alice Aliceville"),
    Painter: Painter("Bob Bobsville"),
    Plumber: Plumber("Craig Craigsville"),
}
for homeowner in homeowners:
    for need in homeowner.needs:
        if need in specialist:
            homeowner.add_specialist(specialist[need])
 

print(alfred.contracts)
print(bert.contracts)
print(candice.contracts)

