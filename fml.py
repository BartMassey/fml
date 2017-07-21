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
        self.title = row[0]
        self.cost = int(row[1])
        self.value = float(row[2])
        self.best_prob = 0.0

# Get the lineup.
lineup_file = sys.stdin
if len(sys.argv) >= 2:
    fn = sys.argv[1]
    v = sys.version_info[0]
    if v == 2:
        lineup_file = open(fn, "rb")
    elif v == 3:
        lineup_file = open(fn, newline="")
    else:
        assert False
reader = csv.reader(lineup_file)
movies = [Movie(row) for row in reader]
# Add the option of an empty screen.
movies += [Movie(('[empty screen]', 0, -2.0))]

# Set the best-performer probabilities.
pmass = 0.0
for m in movies:
    if m.cost == 0:
        continue
    p = m.value * 10 / m.cost
    if p > 0.0:
        m.best_prob = p
        pmass += p
for m in movies:
    if m.best_prob > 0.0:
        m.best_prob /= pmass

# Do a depth-first search of the remaining list finding the
# best number of showings of the given movie index with the
# given screen and dollar budget.  Returns a value
# and the corresponding lineup.
def opt_lineup(movie, screens, budget):
    assert screens <= 8
    assert budget >= 0
    assert movie < len(movies)
    # Base case: out of screens.
    if screens <= 0:
        return (0, [])
    m = movies[movie]
    cost = m.cost
    # Base case: hit the empty screen.
    # Fill the remaining space with empty screens.
    if cost == 0:
        return (screens * m.value, [(screens, movie)])
    value = m.value + m.best_prob * 2.0
    max_showings = min(screens, int(budget // cost))
    best_value = None
    best_lineup = None
    for showings in range(max_showings + 1):
        next_budget = budget - showings * cost
        next_screens = screens - showings
        next_value, next_lineup = \
          opt_lineup(movie + 1, next_screens, next_budget)
        next_value += showings * value
        if best_value == None or next_value > best_value:
            best_value = next_value
            if showings > 0:
                best_lineup = [(showings, movie)] + next_lineup
            else:
                best_lineup = next_lineup
    assert best_value != None
    return (best_value, best_lineup)

# Show the estimate.
value, lineup = opt_lineup(0, 8, 1000)
for n, m in lineup:
    print(n, movies[m].title)
print("$%.1fM" % (value,))
