```markdown
# 📰 News Topic Classification

---

## 🔍 Motivation

News content is growing exponentially across digital platforms. Automatically organizing and classifying news articles is essential for search, recommendation systems, and information retrieval.

Traditional methods rely on **TF-IDF and statistical models**, while modern NLP uses **transformers like BERT** to capture contextual meaning. This project explores the performance gap and trade-offs between traditional feature engineering and deep contextual embeddings.

---

## 🧠 Research Question

**How do traditional machine learning models compare with transformer-based models in news topic classification, and where do traditional models fail?**

---

## 🧪 Methodology

### **1. Dataset**

We use the **AG News dataset**, a benchmark for text classification containing labeled news articles across four categories:

* **World**
* **Sports**
* **Business**
* **Technology**

**Dataset Scale:**
* **Training samples:** ~120,000
* **Test samples:** ~7,600

---

### **2. Text Representation**

#### **TF-IDF (Statistical Baseline)**

$$
tfidf(t,d) = tf(t,d) \cdot \log \frac{N}{df(t)}
$$

Captures word importance based on inverse document frequency, ignoring word order.

#### **Contextual Embedding (BERT)**

$$
H = \text{BERT}(X)
$$

Utilizes the **Bidirectional Encoder Representations from Transformers** to learn deep contextualized syntax and semantics.

---

### **3. Classification Models**

* **Baseline:** Zero-R (Most Frequent Class).
* **Traditional Models:** Naive Bayes, Logistic Regression (with TF-IDF).
* **Transformer Model:** Fine-tuned `bert-base-uncased`.

---

### **4. Evaluation Metrics**

The primary metric is **Accuracy**:

$$
Accuracy = \frac{\text{Correct Predictions}}{\text{Total Predictions}}
$$

We also compute the **F1-score** to account for potential class imbalances in misclassification.

---

### **5. Error Analysis**

We analyze misclassified examples to identify:
* Confusion between semantically similar categories (e.g., Business vs. Tech).
* Impact of ambiguous wording on statistical vs. neural models.
* Model limitations regarding short text snippets.

---

## 📁 Project Structure

```text
news_classification/
│
├── data/                           # Dataset (train/test splits)
│   ├── train.csv
│   └── test.csv
│
├── preprocessing/                  # Text cleaning & tokenization
│   ├── clean_text.py
│   └── tokenizer.py
│
├── models/                         # Model implementations
│   ├── naive_bayes.py
│   ├── logistic_regression.py
│   └── bert_model.py
│
├── analysis/                       # Statistical analysis & error tracking
│   ├── metrics.py
│   └── error_analysis.py           # Confusion matrix & misclassification logs
│
├── experiments/                    # Execution pipeline
│   ├── train.py
│   └── run_experiments.py
│
├── notebooks/                      # Exploratory Data Analysis (EDA)
│   └── news_analysis.ipynb
│
├── results/                        # Saved outputs
│   ├── logs/                       # Training logs
│   └── plots/                      # Confusion matrices & loss curves
│
├── writeup/                        # Academic report
│   ├── report.pdf
│   └── report.md
│
├── presentation/                   # Presentation materials
│   ├── slides.pptx
│   └── slides_notes.md
│
├── requirements.txt                # Python dependencies
├── README.md                       # Project overview
└── LICENSE                         # MIT License
```

---

## ⚙️ Installation

Clone the repository:

```bash
git clone [https://github.com/](https://github.com/)<your-username>/news-classification.git
cd news-classification
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ Running Experiments

### **1. Preprocess Data**

```python
from preprocessing.clean_text import clean_payload
cleaned_text = clean_payload("Apple reports strong quarterly earnings.")
```

### **2. Train a model**

```bash
python experiments/train.py --model bert  # Options: nb, lr, bert
```

### **3. Evaluate performance**

```bash
python analysis/error_analysis.py --model bert
```

### **4. Run full experiment pipeline**

```bash
python experiments/run_experiments.py
```

---

## 📊 Results Summary

* **Non-linearity:** Neural models capture complex semantic relationships that TF-IDF misses.
* **Efficiency:** Logistic Regression remains a strong, fast baseline for clean text.
* **Context:** BERT excels in ambiguous cases (e.g., "Apple" as Business vs. Technology).

| Model | Accuracy | F1-Score |
| :--- | :--- | :--- |
| **Baseline** | ~25.0% | - |
| **Naive Bayes** | ~80.2% | 0.80 |
| **Logistic Regression** | ~88.5% | 0.88 |
| **BERT (Fine-tuned)** | **~93.4%** | **0.93** |

---

## 🔍 Classification Example

**Input:**
> "Apple reports strong quarterly earnings driven by iPhone sales."

**Model Prediction:**
> `Business`

---

## 🛠️ Tech Stack

* **Language:** Python 3.9+
* **Deep Learning:** PyTorch, HuggingFace Transformers
* **Machine Learning:** Scikit-learn
* **NLP:** NLTK, spaCy

---

## 📘 Report

See:
```text
writeup/report.pdf
```

---

## 🎤 Presentation Slides

See:
```text
presentation/slides.pptx
presentation/slides_notes.md
```

---

## 📚 References

* **BERT:** Devlin et al. (2019). *Pre-training of Deep Bidirectional Transformers for Language Understanding*.
* **Text CNN:** Kim, Y. (2014). *Convolutional Neural Networks for Sentence Classification*.
* **Dataset:** Zhang et al. (2015). *Character-level Convolutional Networks for Text Classification*.

---

## ✨ Author

**Gordon Zou**
New York University

---

## 📄 License

MIT License

This project was developed as part of coursework at New York University (NYU). 
NYU does not claim ownership or endorsement of this software.
```
