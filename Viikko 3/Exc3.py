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

earthquake_cpt = {
    (): 1/111
}

burglar_cpt = {
    (): 1/365
}

alarm_cpt = {
    (False, False): 0.0095,
    (True, False): 0.81,
    (False, True): 0.92,
    (True, True): 0.97
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

class EarthquakeModel:
    def __init__(self):
        self.variables = [
        Variable("Earthquake", [], earthquake_cpt),
        Variable("Burglar", [], burglar_cpt),
        Variable("Alarm", ["Earthquake", "Burglar"], alarm_cpt),
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

model = EarthquakeModel()

samples = generate_tuples(1000000, model)

p1 = conditional_probability(
    samples,
    ("Burglar", True),
    {"Alarm": True}
)

p2 = conditional_probability(
    samples,
    ("Burglar", True),
    {"Alarm": True, "Earthquake": True}
)

print("P(B | A):", p1)
print("P(B | A,E):", p2)

'''
3.
What is the probability that a burglar has broken into the home, given that an alarm went off
What is the probability that a burglar has broken into the home, given that an alarm went off and earthquake has happened

4.
P(B | A): 0.13908355795148247
P(B | A,E): 0.007352941176470588
These show that the second is a smaller fraction
This makes sense, since it's unlikely that both erathquake and burglary happen on the same day to lead to an alarm

5. N = 100 000
1. 
P(B | A): 0.13602550478214664
P(B | A,E): 0.002824858757062147
2.
P(B | A): 0.14623115577889448
P(B | A,E): 0.004137931034482759
3.
P(B | A): 0.14382845188284518
P(B | A,E): 0.0028694404591104736

N = 1 000 000
1.
P(B | A): 0.13030161449410788
P(B | A,E): 0.0036452004860267314
2.
P(B | A): 0.13310651661868622
P(B | A,E): 0.002594210813762971
3.
P(B | A): 0.13248931957903512
P(B | A,E): 0.0034626038781163434

Increasing n reduces the spreads
'''