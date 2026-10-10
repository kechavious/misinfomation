# GitHub repository profile

The intended About settings are stored in `.github/repository-profile.json`.
This file documents the settings; GitHub does not apply it automatically.

## Display title

**Network Topology and Finite-Horizon Diffusion Dynamics**

A Reproducible Computational Study of Random, Scale-Free, and Small-World Networks.

The README, paper and citation metadata use this title. The GitHub repository
URL remains unchanged. Academic positioning describes the research methods;
it does not imply an unverified degree enrollment or publication status.

## Description

> Computational network-science research on topology-dependent, finite-horizon SI diffusion, with independent graph replication, uncertainty quantification, and reproducible experiments.

## Topics

`misinformation`, `network-science`, `diffusion`, `simulation`,
`reproducible-research`, `python`, `networkx`, `small-world-networks`, `complex-networks`,
`stochastic-processes`, `computational-social-science`

## Apply the settings

Use the repository's About editor on GitHub, or run the following command with
an authenticated GitHub CLI account that can edit the repository:

```bash
gh repo edit kechavious/misinfomation \
  --description 'Computational network-science research on topology-dependent, finite-horizon SI diffusion, with independent graph replication, uncertainty quantification, and reproducible experiments.' \
  --add-topic misinformation \
  --add-topic network-science \
  --add-topic diffusion \
  --add-topic simulation \
  --add-topic reproducible-research \
  --add-topic python \
  --add-topic networkx \
  --add-topic small-world-networks \
  --add-topic complex-networks \
  --add-topic stochastic-processes \
  --add-topic computational-social-science
```

The command adds the listed topics without removing existing topics. Verify the
About panel after applying it. No separate project website is currently deployed,
so the homepage field is left unchanged; the README links to the paper and
notebook. Avoid a localhost address or a fictitious live-demo link.
