# fml - A Fantasy Movie League™ Solver
Copyright (c) 2017 Po Huit

`fml` is a Python program that optimizes
[*Fantasy Movie League™*](http://fantasymovieleague.com)
picks. The solver finds an optimal lineup given prices and
predictions: both prices and predictions must be provided by
the user.

Note that
[Fantasy Movie League Analyzer](http://analyzer.fmlnerd.com/)
is a web-based tool that provides most of the functionality
of this tool, as well as a comparables finder, all with a
lovely GUI. You should probably just use that unless you
really want to nerd out. Let me know what features you are
still wishing for in my Github
[Issue Tracker](http://github.com/PoHuit/FML/issues), and
I'll see what I can do. Patches are especially welcome.

## Usage

This program should work with Python 2, Python 3 or
[PyPy](http://pypy.org). (Python 2 is likely to be fastest,
while PyPy is likely slowest [!] due to compilation time.)
Try `fml` out on the provided sample by running

      python fml.py lineup.csv

The input may also be provided on standard input.

### Input

The input is a
[CSV](http://en.wikipedia.org/wiki/Comma-separated_values)
file. Each row contains the name of the movie, the price of
the movie in dollars, and predicted values for that movie in
millions of dollars (fractions are ok, can be preceded with
a dollar sign). A movie can have several predictions,
separated by slashes. All but the last should have a percent
probability of that prediction, separated by a percent sign
from the value. The last value gets the rest of the
probability.

### Output

The
output for the provided sample input should look like this:

      1x Mr. Hero [Sun] (VR 1.04, BP 7%)
      3x Car Heists (VR 1.06, BP 7%)
      2x Carbots (VR 1.14, BP 7%)
      2x The Dwelling Horror (VR 1.30, BP 9%)
      $110.0M

The entries here are the number to pick, the film title, the
*value ratio* (expected return in dollars/FMLbuck, with
10M/1 being 1.0), and the *Best Performer probability*
estimated percentage.


## Background

I follow Wilhelm Arcturus's excellent blog
[*The Ancient Gaming Noob*](http://tagn.wordpress.com), and
have been really interested and amused by his reports on the
*Fantasy Movie League™* game he and his friends have been
playing.

I started playing with a Linear Programming solver a while
back with the idea of bringing some mathematical
optimization to FML players. Only after building a program
for [`lp_solve`](http://lpsolve.sourceforge.net) did I
understand the rules well enough to get that the objective
is not linear. The penalty for blank screens and the bonus
for screens with the best bargain need to be included in the
objective function. These bonuses and penalties make it
nonlinear (and non-differentiable).

The only open source code for dealing with linear
constraints and nonlinear objectives I could find in a quick
search was written in FORTRAN and looked to be really hard
to use.

So I wrote from scratch the solver you see here. I
eventually joined Wilhelm's League, and will be updating
this tool as I play my first season. In my warmup the last
week of the current season, this tool guided me to an
almost-best lineup.

## Notes

The exchange rate between price and value appears to be
$100K box-office per dollar in showing cost.

This solver uses memoized depth-first search in the space of
screen assignments. The solver is not algorithmically
super-efficient. However, the instance size here is small so
it turns out not to matter.

I used Python, because apparently I wanted my program to be
as slow as feasible. Turns out it's plenty fast anyhow,
running in less than 0.1s in Python 2 on the provided sample
lineup on my box.

The solver takes the $2M penalty per empty screen into
account, as well as the $2M bonus per best-performer
screening. The bonus is handled probabilistically, computing
an expected return based on the ratio of the
positive-performing estimates converted to a probability.

This solver handles only the easy part of the
problem. Getting good estimates to feed it is the real
challenge, and the whole point of FML. Probably a machine
learner could be trained, but I'm out of energy — I'll leave
that task to other, even geekier FML afficionados.

My current direction for this tool is faster search to
support bigger, automatically generated ensembles for better
reliability.

## License

This program is licensed under the GPL version 3 or later.
Please see the file COPYING in the source distribution of
this software for license terms.
