# GitHub repository profile

The intended About settings are stored in `.github/repository-profile.json`.
This file documents the settings; GitHub does not apply it automatically.

## Description

> Reproducible simulations of information diffusion on random, scale-free, and small-world networks, with seeded experiments, uncertainty analysis, and a research report.

## Topics

`misinformation`, `network-science`, `diffusion`, `simulation`,
`reproducible-research`, `python`, `networkx`, `small-world-networks`

## Apply the settings

Use the repository's About editor on GitHub, or run the following command with
an authenticated GitHub CLI account that can edit the repository:

```bash
gh repo edit kechavious/misinfomation \
  --description 'Reproducible simulations of information diffusion on random, scale-free, and small-world networks, with seeded experiments, uncertainty analysis, and a research report.' \
  --add-topic misinformation \
  --add-topic network-science \
  --add-topic diffusion \
  --add-topic simulation \
  --add-topic reproducible-research \
  --add-topic python \
  --add-topic networkx \
  --add-topic small-world-networks
```

The command adds the listed topics without removing existing topics. Verify the
About panel after applying it. No separate project website is currently deployed,
so the homepage field is left unchanged; the README links to the paper and
notebook. Avoid a localhost address or a fictitious live-demo link.
