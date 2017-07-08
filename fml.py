import csv
from sys import stdin

class Movie():
    def __init__(self, row):
        self.abbrev = row[0]
        self.cost = int(row[1])
        self.value = float(row[2])

# Get the lineup.
reader = csv.reader(stdin)
movies = {row[0]: Movie(row) for row in reader}

def lineup_value(lineup):
    screens = 0
    value = 0
    for abbrev in lineup:
        showings = lineup[abbrev]
        screens += showings
        value += showings * movies[abbrev].value
    return value - 2.0 * (8 - screens)

def lineup_screens(lineup):
    screens = 0
    for abbrev in lineup:
        screens += lineup[abbrev]
    return screens

def best_lineup(remaining, lineup, budget):
    screens = lineup_screens(lineup)
    if screens < 0 or screens > 8:
        print("bad screens", screens)
        assert False
    if remaining == [] or screens == 8:
        return dict(lineup)
    best = dict(lineup)
    best_value = lineup_value(lineup)
    target = remaining.pop()
    cost = movies[target].cost
    max_showings = min(8 - screens, budget // cost)
    for showings in range(max_showings + 1):
        next_budget = budget - showings * cost
        if showings > 0:
            lineup[target] = showings
        opt_lineup = best_lineup(list(remaining), lineup, next_budget)
        opt_value = lineup_value(opt_lineup)
        if opt_value > best_value:
            best = opt_lineup
            best_value = opt_value
    if target in lineup:
        del lineup[target]
    return best

answer = best_lineup(list(movies), dict(), 1000)
for m in answer:
    print(m, answer[m])
print(lineup_value(answer))
