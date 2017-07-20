# Copyright (c) 2017 Po Huit
# [This program is licensed under the GPL version 3 or later.]
# Please see the file COPYING in the source
# distribution of this software for license terms.

# Compute an optimal lineup for Fantasy Movie League
# from performance estimates.

from __future__ import print_function

import csv
import sys

# Record of information about a movie.
class Movie():
    def __init__(self, row):
        self.abbrev = row[0]
        self.cost = int(row[1])
        self.value = float(row[2])
        self.best_prob = 0.0

# Get the lineup.
reader = csv.reader(sys.stdin)
movies = {row[0]: Movie(row) for row in reader}

# Set the best-performer probabilities.
pmass = 0.0
for abbrev in movies:
    m = movies[abbrev]
    p = m.value * 10 / m.cost
    if p > 0.0:
        m.best_prob = p
        pmass += p
for abbrev in movies:
    m = movies[abbrev]
    if m.best_prob > 0.0:
        m.best_prob /= pmass

# The estimated value of the given lineup.
def lineup_value(lineup):
    screens = 0
    value = 0
    for abbrev in lineup:
        movie = movies[abbrev]
        showings = lineup[abbrev]
        screens += showings
        value += showings * (movie.value + 2.0 * movie.best_prob)
    return round(value - 2.0 * (8 - screens), 1)

# Number of screens used in the given lineup.
def lineup_screens(lineup):
    screens = 0
    for abbrev in lineup:
        screens += lineup[abbrev]
    return screens

# Do a depth-first search (from back-to-front)
# of the remaining list finding the best augmentation
# of the given lineup under the given budget.
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

# Show the estimate.
answer = best_lineup(list(movies), dict(), 1000)
for m in answer:
    print(answer[m], m)
print(lineup_value(answer))
