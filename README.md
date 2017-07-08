# FML - A Fantasy Movie League™ Solver

I started playing with a Linear Programming solver a few
days ago with the idea of bringing some mathematical
optimization to
[*Fantasy Movie League*](http://fantasymovieleague.com). Only
after building a program for
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

So I wrote this brute-force depth-first search solver. I
used Python 3, because apparently I wanted it to be as slow
as feasible. Turns out it's plenty fast anyhow, running in
about 2s on a sample lineup on my box. Aside from rewriting
it in Rust, there's plenty of optimizations available if it
turns out to be too slow someday. I don't think it will.

The input (on standard input) is a CSV file. Each row
contains the name of the movie, the price of that movie, and
your predicted value for that movie in millions of dollars
(fractions are ok). Note that the exchange rate between
price and value appears to be $100K box-office per dollar in
showing cost. All the solver does is find an optimal lineup
given your predictions.

The solver takes the $2M penalty per empty screen into
account. The solver takes the $2M bonus per best-performer
screening into account probabilistically, computing it
automatically as an expected return based on the ratio of
the positive-performing estimates.
