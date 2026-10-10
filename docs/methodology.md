# Model and experimental design

## Scope

This project studies diffusion on synthetic undirected networks. It does not
classify content, distinguish truth from falsehood, estimate platform behavior,
or predict real-world virality. “Misinformation” describes the motivating
application, not a property inferred from observations.

## Synchronous SI diffusion

A single uniformly sampled node is adopted at time zero. During each round,
every adopted node attempts transmission to every susceptible neighbor,
independently, with probability `p`. Newly adopted nodes become active in the
next round. Adoption is permanent, and attempts repeat in subsequent rounds.
The process continues through the configured horizon even if a round has no
new adoptions. Multiple infected neighbors can attempt to infect the same node.

For a node with `k` adopted neighbors, the conditional probability of adoption
in one round is `1 - (1 - p)^k`. Outcomes include the initial source. With `p=0`,
adoption is `1/n`; with `p=1`, adoption expands one graph-distance step per round.
This is a discrete-time susceptible–infected model, not an independent-cascade
model (which typically allows only one attempt per newly active edge).

## Network comparison

- **ER:** `G(n, 8/(n-1))`, expected mean degree 8.
- **BA:** preferential attachment with `m=4`, mean degree approaching 8.
- **Optional WS:** `k=8`, rewiring probability in `{0, .01, .1, .5, 1}`.

ER and BA have approximately matched mean degree, not matched degree sequences
or identical realized edge counts. Disconnected graphs are retained; component
coverage is recorded. WS rewiring keeps the number of edges fixed but changes
clustering, path lengths and other properties simultaneously. Its results are
an association under a rewiring intervention, not an isolated causal effect of
clustering.

## Replication and uncertainty

Defaults: 800 nodes, 5 independent graphs per configuration, 30 independent
source/diffusion runs per probability and graph, 21 probabilities from 0 to 1,
10 rounds, master seed 42. Network and diffusion seeds are recorded for every
trial. The local PRNG does not mutate global random state.

First average the 30 runs within each graph. Then average the five graph-level
means. The shaded band is a 95% Student-t interval across those graph means,
clipped to the valid fraction range `[0,1]`. It estimates uncertainty in mean
adoption over random graphs and trials, not the range of individual cascades.
Five graph replicates give a coarse uncertainty estimate; increase `--graphs`
for stronger inference. The intervals are pointwise, not simultaneous bands.

## Two distinct summaries

**Empirical 80% threshold:** first sampled `p` whose mean adoption is at least
0.8. It is grid dependent (default resolution 0.05), has no threshold confidence
interval in this workflow, and is left empty if the sampled curve never reaches
0.8. It is a finite-horizon operational summary, not proof of a phase transition.

**Logistic midpoint:** least-squares fit of
`A(p) = expit(alpha * (p - p0))`, with nonnegative slope and `p0` constrained to
`[0,1]`. `p0` is the fitted 50% midpoint. It is not the 80% threshold and the
fit is descriptive, not logistic regression on observed binary outcomes. Fits
record mean squared error and any failure; flat curves or curves that do not
bracket 50% adoption are not fitted.

## Reproducibility and limitations

The CLI writes per-trial data, graph properties, mean curves, summary statistics,
figures and metadata with dependency versions and CSV SHA-256 hashes. All random
sampling derives from the master seed. CSVs replay exactly under the tested
Python/dependency versions; timestamps and rendered image metadata need not be
byte-identical. Pinned direct dependencies are in `requirements.txt`; transitive
dependencies are not fully locked.

Synthetic static graphs, homogeneous transmission probabilities, one random
seed node and permanent adoption simplify behavior considerably. This model
omits recommender systems, recovery, fact-checking, temporal edges, user
heterogeneity and content semantics. Comparisons do not establish universal
claims about platforms, finite-size scaling or clustering causality. No external
simulator validation or real-data calibration is claimed.
