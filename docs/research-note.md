# Network topology and finite-horizon diffusion

## Question and design

The current study asks how synthetic network structure changes adoption under
one synchronous, repeated-attempt SI process. ER and BA networks are generated
with approximately matched mean degree. Five independent graphs per
configuration each receive 30 trials at every probability on a 21-point grid.
All networks contain 800 nodes; the time horizon is ten rounds.

Unlike the original coursework, this version records every random seed and trial,
uses the same implementation in scripts and notebooks, and distinguishes an
empirical 80% adoption threshold from a fitted logistic midpoint.

## Findings from the reference run

ER's fitted midpoint is about 0.139; BA's is about 0.111. BA's hub structure is
consistent with earlier growth under these conditions. The experiment alone
does not identify a unique mechanism or support extrapolation to real platforms.
Both reach 80% mean adoption at p=0.20 on the grid with spacing 0.05. A finer grid
could resolve differences that this summary does not detect.

The WS lattice and low-rewiring configuration fail to reach 80% adoption within
ten rounds, even at p=1. Local propagation and the finite time horizon constrain
coverage. At beta=0.1 the sampled threshold is 0.35; at beta=0.5 and 1 it is 0.20.
Rewiring simultaneously changes clustering and shortest paths, so these outcomes
cannot be attributed to clustering alone.

The SI process permits repeated transmission attempts and permanent adoption.
Longer horizons can materially shift results; they should be studied rather
than assumed equivalent. Numerical S-shaped curves do not by themselves prove
a phase transition or validate a real-world misinformation model.

## Evidence and uncertainty

The checked-in `results/` contains 22,050 individual outcomes, graph properties,
mean curves, summary metrics and metadata with hashes. Shaded comparison bands
are pointwise Student-t intervals over graph-level means, not individual trial
ranges or confidence intervals for the thresholds. Five graph replicates are a
starting point; stronger claims require greater replication and sensitivity
analysis. Curves not bracketing 50% adoption receive no fitted midpoint.

## Conclusion

Network topology can alter finite-horizon adoption under a transparent,
specified transmission model. This project provides a reproducible framework
for testing that relationship and extending it, while separating observed
simulation outcomes from claims requiring additional evidence.
