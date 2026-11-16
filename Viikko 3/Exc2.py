'''
 generate_tuples(n, model):
1:    for i = 1 to n:
2:       v = empty array
3:       for V in model.variables:
4:          pa = v[V.Pa]    # parents of V
5:          v.append(sample(V.CPT(pa)))
6:       output v
'''
import random

battery_cpt = {
    (): 0.9
}

radio_cpt = {
    (False,): 0.0,
    (True,): 0.9
}

ignition_cpt = {
    (False,): 0.0,
    (True,): 0.95
}

gas_cpt = {
    (): 0.95
}

starts_cpt = {
    (False, False): 0.0,
    (False, True): 0.0,
    (True, False): 0.0,
    (True, True): 0.99
}

moves_cpt = {
    (False,): 0.0,
    (True,): 0.99
}

def sample(probability):
    return random.random() < probability
    
class Variable:
    def __init__(self, name, parents, cpt):
        self.name = name
        self.parents = parents
        self.cpt = cpt
    
    def getCPT(self):
        return self.cpt
        
    def getParents(self):
        return self.parents

class CarModel:
    def __init__(self):
        self.variables = [
        Variable("Battery", [], battery_cpt),
        Variable("Radio", ["Battery"], radio_cpt),
        Variable("Ignition", ["Battery"], ignition_cpt),
        Variable("Gas", [], gas_cpt),
        Variable("Starts", ["Ignition", "Gas"], starts_cpt),
        Variable("Moves", ["Starts"], moves_cpt)
        ]
    def getVariables(self):
        return self.variables

def generate_tuples(n, model):
    tuples = []
    for i in range(n):
        v = {}
        for V in model.getVariables():
            pa = tuple(v[parent] for parent in V.getParents())
            probability = V.getCPT()[pa]
            sampled = sample(probability)
            v[V.name] = sampled
        tuples.append(v)
    return tuples


def filter_samples(samples, condition):
    return [
        s for s in samples
        if all(s[var] == value for var, value in condition.items())
    ]

def conditional_probability(samples, query, condition):
    filtered = filter_samples(samples, condition)

    if len(filtered) == 0:
        return None

    variable, value = query

    matching = sum(
        1 for s in filtered
        if s[variable] == value
    )

    return matching / len(filtered)

model = CarModel()

samples = generate_tuples(100000, model)

p1 = conditional_probability(
    samples,
    ("Battery", True),
    {"Radio": True, "Gas": True, "Starts": False}
)

p2 = conditional_probability(
    samples,
    ("Starts", True),
    {"Radio": True, "Ignition": True, "Gas": True}
)

p3 = conditional_probability(
    samples,
    ("Starts", True),
    {"Radio": False, "Ignition": True, "Gas": True}
)

print("P(B | R,G,¬S):", p1)
print("P(S | R,I,G):", p2)
print("P(S | ¬R,I,G):", p3)