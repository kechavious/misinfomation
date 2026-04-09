Online misinformation spreads rapidly across social platforms such as Twitter, Reddit, TikTok, and Instagram. Understanding when false information becomes viral is essential for platform moderation, algorithm design, and public policy.

This project investigates the tipping point — the critical resharing probability at which misinformation transitions from localized spread to global cascades.

🧠 Research Question



Does misinformation diffusion exhibit a nonlinear tipping point, and how do different network structures influence it?

🧪 Methodology



1. Network Generation



We study two classic network topologies:

Erdős–Rényi (ER) Random Network



G(n,pe)

Represents decentralized, homogeneous online communities.

Barabási–Albert (BA) Scale-Free Network



P(k)∼k−3

Represents influencer-driven platforms like Twitter.

2. Diffusion Model (Agent-Based)



Each node reshares misinformation with probability ( p ) once exposed.

State update:

Xi(t+1)={1if exposed and reshared with probability p0otherwise

Adoption rate:

A(p)=number of nodes resharedn

3. Tipping Point Definition



We define the empirical tipping point as:

pt=minp∣A(p)≥0.8

4. Logistic Model Fitting



Adoption curve is modeled using:

A(p)=11+e−α(p−p0)

Where:

α: diffusion steepnessp0: inflection point (estimated tipping point)

Inflection point:

p0=arg⁡max(dAdp)

5. Clustering Analysis



Clustering coefficient:

C=3×trianglesconnected triples

Higher clustering → delayed tipping point.

📁 Project Structure





misinformation_spread_sim/

│

├── data/ # (Optional) External datasets / configuration files

│ └── README.md # Description of data sources

│

├── simulation/ # Core simulation engine

│ ├── build_networks.py # ER / BA network generation functions

│ ├── run_diffusion.py # Agent-based diffusion simulation

│ └── utils.py # Sweep functions, random seed control, helpers

│

├── analysis/ # Statistical analysis & modeling

│ ├── fit_logistic.py # Logistic regression for tipping point estimation

│ ├── compute_metrics.py # Adoption curve computation, derivatives, metrics

│ └── clustering_analysis.py # Clustering coefficient → tipping point relationship

│

├── notebooks/ # Reproducible research notebooks

│ └── misinformation_analysis.ipynb # Full experiment workflow (ER, BA, logistic fit, clustering)

│

├── results/ # Saved numerical outputs & generated figures

│ ├── csv/ # Adoption curves, tipping points, clustering results

│ └── plots/ # PNG visualizations for experiments

│

├── writeup/ # Academic paper version

│ ├── paper.md # Markdown draft of the research paper

│ └── paper.pdf # Final PDF formatted paper

│

├── presentation/ # Final presentation materials

│ ├── slides.pptx # Full 10–12 minute presentation

│ └── slides_notes.md # Speaker notes for live talk

│

├── requirements.txt # Python dependencies for reproducibility

├── README.md # Project overview, setup, results summary

└── LICENSE # MIT license (or chosen open-source license)



⚙️ Installation



Clone the repository:

git clone https://github.com/<your-username>/misinformation_spread_sim.gitcd misinformation_spread_sim



Install dependencies:

pip install -r requirements.txt



▶️ Running Simulations



1. Generate a network



from simulation.build_networks import build_er_networkG = build_er_network(n=10000, p_edge=0.01)



2. Run diffusion



from simulation.run_diffusion import simulate_diffusionrate = simulate_diffusion(G, p=0.15, num_rounds=10)print(rate)



3. Sweep probabilities



from simulation.utils import sweep_probabilitiescurve = sweep_probabilities(G, [i/100 for i in range(1, 40)], runs=30, sim_func=simulate_diffusion)



4. Fit logistic model



from analysis.fit_logistic import fit_logisticalpha, p0 = fit_logistic(list(curve.keys()), list(curve.values()))print("Estimated tipping point:", p0)



5. Clustering vs Tipping



from analysis.clustering_analysis import clustering_vs_tippingC, p_t = clustering_vs_tipping(G, [i/100 for i in range(1, 40)], sim_func=simulate_diffusion)print(C, p_t)



📊 Results Summary



Misinformation diffusion is nonlinear, following an S-curve.

BA networks tip earlier due to high-degree hubs.

ER networks require higher resharing probability to cascade.

Logistic model accurately identifies tipping probability.

High clustering increases resistance to global spread.

📘 Academic Paper



See:

writeup/paper.pdf



🎤 Presentation Slides



See:

presentation/slides.pptx

presentation/slides_notes.md



📚 References



A Simple Model of Global Cascades on Random Networks — D. J. Watts (2002): https://www.pnas.org/doi/10.1073/pnas.082090499 (PNAS)

The Spread of Behavior in an Online Social Network Experiment — D. Centola (2010): https://www.science.org/doi/10.1126/science.1185231

FakeNews Simulator (GitHub): https://github.com/FraLotito/fakenews_simulator

Fake‑News‑Network‑Modeling (GitHub): https://github.com/kymry/Fake-News-Network-Modeling

Epidemics and Rumours — D.J.Daley & D.G.Kendall (1965): https://www.nature.com/articles/2041118a0

✨ Author



Gordon Zou

New York University



📄 License



MIT License

This project was developed as part of coursework at New York University (NYU). NYU does not claim ownership or endorsement of this software.



幫著我把這個修改成類似於上面的格式

```markdown

# 📰 News Topic Classification



---



## 🔍 Motivation



News content is growing exponentially across digital platforms. Automatically organizing and classifying news articles is essential for search, recommendation systems, and information retrieval.



Traditional methods rely on **TF-IDF and statistical models**, while modern NLP uses **transformers like BERT** to capture contextual meaning.



This project explores the performance gap between these approaches.



---



## 🧠 Research Question



**How do traditional machine learning models compare with transformer-based models in news topic classification?**



---



## 🧪 Methodology



### **1. Dataset**



We use the **AG News dataset**, containing labeled news articles across four categories:



- World  

- Sports  

- Business  

- Technology  



Dataset size:

- ~120,000 training samples  

- ~7,600 test samples  



---



### **2. Text Representation**



#### **TF-IDF Representation**



$$

tfidf(t,d) = tf(t,d) \cdot \log \frac{N}{df(t)}

$$



Captures word importance based on frequency.



---



#### **Contextual Embedding (BERT)**



$$

H = \text{BERT}(X)

$$



Learns deep contextual representations of text.



---



### **3. Classification Models**



#### **Baseline**



- Most Frequent Class



#### **Traditional Models**



- Naive Bayes  

- Logistic Regression (TF-IDF)



#### **Transformer Model**



- Fine-tuned BERT  



---



### **4. Evaluation Metrics**



Accuracy:



$$

Accuracy = \frac{\text{Correct Predictions}}{\text{Total Predictions}}

$$



Precision / Recall / F1-score are also used for detailed evaluation.



---



### **5. Error Analysis**



We analyze misclassified examples to identify:



- Confusion between categories  

- Ambiguous wording  

- Model limitations  



---



## 📁 Project Structure



```



news_classification/

│

├── data/                           # Dataset (train/test splits)

│   ├── train.csv

│   ├── test.csv

│

├── preprocessing/                  # Text preprocessing

│   ├── clean_text.py

│   ├── tokenizer.py

│

├── models/                         # Model implementations

│   ├── naive_bayes.py

│   ├── logistic_regression.py

│   ├── bert_model.py

│

├── evaluation/                     # Metrics & evaluation

│   ├── metrics.py

│   ├── evaluate.py

│

├── experiments/                    # Experiment pipeline

│   ├── train.py

│   ├── run_experiments.py

│

├── results/                        # Outputs & visualizations

│   ├── logs/

│   ├── plots/

│

├── notebooks/                      # Jupyter experiments

│   └── analysis.ipynb

│

├── requirements.txt

├── README.md

└── LICENSE



````



---



## ⚙️ Installation



```bash

git clone https://github.com/<your-username>/news-classification.git

cd news-classification

pip install -r requirements.txt

````



---



## ▶️ Running Experiments



### **1. Train model**



```bash

python experiments/train.py --model nb

python experiments/train.py --model lr

python experiments/train.py --model bert

```



---



### **2. Evaluate model**



```bash

python evaluation/evaluate.py --model bert

```



---



### **3. Run full experiment pipeline**



```bash

python experiments/run_experiments.py

```



---



## 📊 Results Summary



* Traditional models perform well with TF-IDF features

* Logistic Regression outperforms Naive Bayes

* BERT achieves the highest accuracy due to contextual understanding



| Model               | Accuracy |

| ------------------- | -------- |

| Baseline            | ~25%     |

| Naive Bayes         | ~80%     |

| Logistic Regression | ~88%     |

| BERT                | ~93%     |



---



## 🔍 Example



Input:



```

Apple reports strong quarterly earnings driven by iPhone sales.

```



Output:



```

Business

```



---



## 🛠️ Tech Stack



* Python

* scikit-learn

* PyTorch

* HuggingFace Transformers

* NLTK / spaCy



---



## 📘 Report



See:



```

writeup/report.pdf

```



---



## 🎤 Presentation



See:



```

presentation/slides.pptx

```



---



## 📚 References



* Kim, Y. (2014). CNN for Sentence Classification

* Joulin et al. (2017). FastText

* Zhang et al. (2015). Character-level CNN

* Yang et al. (2016). Hierarchical Attention Networks

* Devlin et al. (2019). BERT



---



## ✨ Author



**Gordon Zou**

New York University



---



## 📄 License



MIT License



```

```
