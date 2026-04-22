---

## 🔍 Motivation

Online misinformation spreads rapidly across social platforms such as
Twitter, Reddit, TikTok, and Instagram. Understanding *when* false
information becomes viral is essential for platform moderation, algorithm
design, and public policy.

This project investigates the **tipping point** — the critical
resharing probability at which misinformation transitions from localized
spread to global cascades.

---

## 🧠 Research Question

**Does misinformation diffusion exhibit a nonlinear tipping point, and how do
different network structures influence it?**

---

## 🧪 Methodology

### **1. Network Generation**

We study two classic network topologies:

#### **Erdős–Rényi (ER) Random Network**

$$
G(n, p_e)
$$


Represents decentralized, homogeneous online communities.

#### **Barabási–Albert (BA) Scale-Free Network**

$$
P(k) \sim k^{-3}
$$


Represents influencer-driven platforms like Twitter.

---

### **2. Diffusion Model (Agent-Based)**

Each node reshares misinformation with probability \( p \) once exposed.

State update:

$$
X_i(t+1) =
\begin{cases}
1 & \text{if exposed and reshared with probability } p \\
0 & \text{otherwise}
\end{cases}
$$



Adoption rate:

$$
A(p)=\frac{\text{number of nodes reshared}}{n}
$$

---

### **3. Tipping Point Definition**

We define the empirical tipping point as:

$$
p_t = \min \{ p \mid A(p) \ge 0.8 \}
$$

---

### **4. Logistic Model Fitting**

Adoption curve is modeled using:

$$
A(p) = \frac{1}{1 + e^{-\alpha(p - p_0)}}
$$

Where:

$$
\begin{aligned}
\alpha &: \text{ diffusion steepness} \\
p_0 &: \text{ inflection point (estimated tipping point)}
\end{aligned}
$$


Inflection point:

$$
p_0 = \arg\max \left( \frac{dA}{dp} \right )
$$


---

### **5. Clustering Analysis**

Clustering coefficient:

$$
C = \frac{3 \times \text{triangles}}{\text{connected triples}}
$$

Higher clustering → delayed tipping point.

---

## 📁 Project Structure

```

misinformation_spread_sim/
│
├── data/                           # (Optional) External datasets / configuration files
│   └── README.md                   # Description of data sources
│
├── simulation/                     # Core simulation engine
│   ├── build_networks.py           # ER / BA network generation functions
│   ├── run_diffusion.py            # Agent-based diffusion simulation
│   └── utils.py                    # Sweep functions, random seed control, helpers
│
├── analysis/                       # Statistical analysis & modeling
│   ├── fit_logistic.py             # Logistic regression for tipping point estimation
│   ├── compute_metrics.py          # Adoption curve computation, derivatives, metrics
│   └── clustering_analysis.py      # Clustering coefficient → tipping point relationship
│
├── notebooks/                      # Reproducible research notebooks
│   └── misinformation_analysis.ipynb   # Full experiment workflow (ER, BA, logistic fit, clustering)
│
├── results/                        # Saved numerical outputs & generated figures
│   ├── csv/                        # Adoption curves, tipping points, clustering results
│   └── plots/                      # PNG visualizations for experiments
│
├── writeup/                        # Academic paper version
│   ├── paper.md                    # Markdown draft of the research paper
│   └── paper.pdf                   # Final PDF formatted paper
│
├── presentation/                   # Final presentation materials
│   ├── slides.pptx                 # Full 10–12 minute presentation
│   └── slides_notes.md             # Speaker notes for live talk
│
├── requirements.txt                # Python dependencies for reproducibility
├── README.md                       # Project overview, setup, results summary
└── LICENSE                         # MIT license (or chosen open-source license)


````

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/kechavious/misinformation_spread_sim.git
cd misinformation_spread_sim
````

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ Running Simulations

### **1. Generate a network**

```python
from simulation.build_networks import build_er_network
G = build_er_network(n=10000, p_edge=0.01)

```

### **2. Run diffusion**

```python
from simulation.run_diffusion import simulate_diffusion
rate = simulate_diffusion(G, p=0.15, num_rounds=10)
print(rate)
```

### **3. Sweep probabilities**

```python
from simulation.utils import sweep_probabilities
curve = sweep_probabilities(G, [i/100 for i in range(1, 40)], runs=30, sim_func=simulate_diffusion)
```

### **4. Fit logistic model**

```python
from analysis.fit_logistic import fit_logistic
alpha, p0 = fit_logistic(list(curve.keys()), list(curve.values()))
print("Estimated tipping point:", p0)
```

### **5. Clustering vs Tipping**

```python
from analysis.clustering_analysis import clustering_vs_tipping
C, p_t = clustering_vs_tipping(G, [i/100 for i in range(1, 40)], sim_func=simulate_diffusion)
print(C, p_t)
```

---

## 📊 Results Summary

* Misinformation diffusion is **nonlinear**, following an S-curve.
* BA networks tip earlier due to high-degree hubs.
* ER networks require higher resharing probability to cascade.
* Logistic model accurately identifies tipping probability.
* High clustering increases resistance to global spread.

---

## 📘 Academic Paper

See:

```
writeup/paper.pdf
```

---

## 🎤 Presentation Slides

See:

```
presentation/slides.pptx
presentation/slides_notes.md
```

---

## 📚 References

* A Simple Model of Global Cascades on Random Networks — D. J. Watts (2002): https://www.pnas.org/doi/10.1073/pnas.082090499 (PNAS)
* The Spread of Behavior in an Online Social Network Experiment — D. Centola (2010): https://www.science.org/doi/10.1126/science.1185231 
* FakeNews Simulator (GitHub): https://github.com/FraLotito/fakenews_simulator
* Fake‑News‑Network‑Modeling (GitHub): https://github.com/kymry/Fake-News-Network-Modeling
* Epidemics and Rumours — D.J.Daley & D.G.Kendall (1965): https://www.nature.com/articles/2041118a0

---

## ✨ Author

**Gordon Zou**
```
New York University
```

---

## 📄 License

MIT License

This project was developed as part of coursework at New York University (NYU).
NYU does not claim ownership or endorsement of this software.


---
