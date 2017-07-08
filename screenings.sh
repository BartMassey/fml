#!/bin/sh
TMP=/tmp/movie-opt-$$.lp
trap "rm -f $TMP" 0 1 2 3 15
python3 screenings.py <lineup.csv >$TMP
lp_solve $TMP
