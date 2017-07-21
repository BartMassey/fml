# FML - A Fantasy Movie League™ Solver
Copyright (c) 2017 Po Huit

FML is a brute-force depth-first solver for optimizing
[*Fantasy Movie League™*](http://fantasymovieleague.com)
picks. The solver finds an optimal lineup given
prices and predictions: both prices and predictions must be
provided by the user.

## Usage

This program requires Python: should work with both Python 2
and Python 3. Try it out on the provided sample by running

      python fml.py lineup.csv

The input may also be provided on standard input. The output
for the sample input looks like this:

      6 Car Heists
      2 Carbots
      $113.2M

The input is a
[CSV](http://en.wikipedia.org/wiki/Comma-separated_values)
file. Each row contains the name of the movie, the price of
the movie in dollars, and a predicted value for that movie
in millions of dollars (fractions are ok). Note that the
exchange rate between price and value appears to be $100K
box-office per dollar in showing cost.

## Background

I follow Wilhelm Arcturus's excellent blog
[*The Ancient Gaming Noob*](http://tagn.wordpress.com), and
have been really interested and amused by his reports on the
*Fantasy Movie League™* game he and his friends have been
playing.

I started playing with a Linear Programming solver a few
days ago with the idea of bringing some mathematical
optimization to FML. Only after building a program for
[`lp_solve`](http://lpsolve.sourceforge.net) did I
understand the rules well enough to get that the objective
is not linear. The penalty for blank screens and the bonus
for screens with the best bargain need to be included in the
objective function, and make it nonlinear (and
non-differentiable).

The only open source code for dealing with linear
constraints and nonlinear objectives I could find in a quick
search was written in FORTRAN and looked to be really hard
to use.

So I wrote the brute-force solver you see here.

I used Python, because apparently I wanted it to be as slow
as feasible. Turns out it's plenty fast anyhow, running in
less than 0.4s on the provided sample lineup on my box —
under 0.2s if I use [PyPy](http://pypy.org).

## Notes

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

## License

This program is licensed under the GPL version 3 or later.
Please see the file COPYING in the source distribution of
this software for license terms.
