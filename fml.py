#!/usr/bin/python2
# Copyright (c) 2017 Po Huit
# [This program is licensed under the GPL version 3 or later.]
# Please see the file COPYING in the source
# distribution of this software for license terms.

# Compute an optimal lineup for Fantasy Movie League
# from performance estimates.

from __future__ import print_function

import csv
import sys

# Strip dollar sign from price string and return as float.
def dollar_float(p):
    if p[0] == '$':
        p = p[1:]
    return float(p)

# Record of information about a movie.
class Movie():
    def __init__(self, row):
        self.title = row[0]
        self.cost = row[1]
        if self.cost != None:
            self.cost = int(self.cost)
        self.values = []
        values = row[2].split("/")
        prob = 0.0
        for pvs in values[:-1]:
            ps, vs = pvs.split("%")
            p = float(ps) / 100.0
            v = dollar_float(vs)
            prob += p
            assert prob < 1.0
            self.values.append((p, v))
        p = 1.0 - prob
        v = dollar_float(values[-1])
        self.values.append((p, v))
        # print(self.title, self.values)

    def ev(self):
        result = 0.0
        for p, v in self.values:
            result += p * v
        return result

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
movies += [Movie(('[empty screen]', None, "-2.0"))]

# Do a memoized depth-first search of the remaining list finding the
# best number of showings of the given movie index with the
# given screen and dollar budget.  Returns a value
# and the corresponding lineup.
memo = dict()
def opt_lineup(movie, screens, budget):
    global memo
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
    if cost == None:
        return (screens * m.ev(), [(screens, movie)])
    # Base case: memo table already has the value we need.
    args = (movie, screens, budget)
    if args in memo:
        return memo[args]
    value = m.ev()
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
    result = (best_value, best_lineup)
    memo[args] = result
    return result

# Show the estimate.
value, lineup = opt_lineup(0, 8, 1000)
for n, m in lineup:
    mm = movies[m]
    if mm.cost != None:
        vr = "%.2f" % (10 * mm.ev() / mm.cost,)
    else:
        vr = "-"
    print("%dx %s (VR %s)" %
          (n, mm.title, vr))
print("$%.1fM" % (value,))
