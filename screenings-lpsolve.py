import csv
from sys import stdin

class Movie():
    def __init__(self, row):
        self.abbrev = row[0]
        self.cost = int(row[1])
        self.value = float(row[2])

# Get the lineup.
reader = csv.reader(stdin)
movies = [Movie(row) for row in reader]


# Show the objective function.
value_terms = [str(m.value * m.cost)  + '*' + m.abbrev \
               for m in movies]
print("max: %s;" % ('+'.join(value_terms),))

# Show the showings constraint.
var_terms = [m.abbrev for m in movies]
print("%s = 8;" % ('+'.join(var_terms),))

# Show the cost constraint.
cost_terms = [str(m.cost)  + '*' + m.abbrev \
              for m in movies]
print("%s <= 1000;" % ('+'.join(cost_terms),))

# Show the variables.
print("int %s;" % (','.join(var_terms),))
