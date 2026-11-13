# Cyber Hacking Breach Modelling and Prediction

A beginner-friendly, defensive machine-learning project that demonstrates how network-traffic characteristics can be analysed to classify records as **potentially suspicious** or **normal**.

> **Important:** The included CSV files contain synthetic demonstration data generated for this repository. They are not real network captures, real incidents, or evidence of actual cyber breaches. The model is an academic prototype, not a production intrusion-detection system.

## Project objectives

- Explore selected network-traffic and connection features.
- Prepare numerical and categorical data for machine learning.
- Train a classification model to identify potentially suspicious records.
- Evaluate the model using a held-out test set.
- Run predictions on a separate CSV file.

## Repository structure

```text
cyber-breach-modelling-prediction/
├── data/
│   └── sample_network_traffic.csv   # Synthetic labelled training data
├── examples/
│   └── new_traffic.csv              # Example records for prediction
├── src/
│   ├── train_model.py               # Preprocessing, training and evaluation
│   └── predict.py                   # Predicts labels for a CSV file
├── models/                          # Trained model is saved here
├── reports/                         # Evaluation and prediction outputs
├── requirements.txt
├── .gitignore
└── README.md
```

## Technology used

- Python
- Pandas
- Scikit-learn
- Joblib
- Machine learning: Random Forest classification

## Dataset fields

| Field | Meaning |
|---|---|
| `duration` | Connection duration in seconds |
| `protocol_type` | Protocol category, such as TCP, UDP or ICMP |
| `service` | Illustrative service category |
| `src_bytes` | Bytes sent from the source |
| `dst_bytes` | Bytes sent to the destination |
| `failed_logins` | Number of failed login attempts associated with the record |
| `connection_count` | Number of connections in the observation window |
| `unusual_port` | Whether an uncommon port was observed (0 or 1) |
| `same_src_dst` | Whether source and destination identifiers match (0 or 1) |
| `label` | Demonstration target: 0 = normal, 1 = potentially suspicious |

These fields are simplified educational features. They do not represent a standard benchmark dataset or a complete set of indicators used by a real SOC.

## Setup

Use Python 3.9 or newer.

### 1. Clone the repository

```bash
git clone https://github.com/Ambati-Anil-13/cyber-breach-modelling-prediction.git
cd cyber-breach-modelling-prediction
```

### 2. Create and activate a virtual environment

**Windows PowerShell:**

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

**Linux / Kali Linux / macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

## Train and evaluate the model

From the project root, run:

```bash
python src/train_model.py
```

The script trains a Random Forest pipeline and prints a classification report and confusion matrix. It saves generated files to:

- `models/breach_prediction_model.joblib`
- `reports/evaluation_metrics.json`
- `reports/feature_importance.csv`

The reported scores measure performance only on this synthetic demonstration dataset. They must not be presented as real-world detection accuracy.

## Predict on new records

After training, run:

```bash
python src/predict.py --input examples/new_traffic.csv
```

The predictions are saved by default to `reports/predictions.csv`. To choose another output path:

```bash
python src/predict.py --input examples/new_traffic.csv --output reports/my_predictions.csv
```

The output contains the predicted class, a human-readable result, and the model's estimated probability for class 1. A probability is a model score, not proof that a breach occurred.

## Limitations and future improvements

- Replace the synthetic data with an appropriately licensed, documented dataset before drawing research conclusions.
- Review class imbalance, false positives and false negatives.
- Validate the model on data collected separately from the training data.
- Add feature engineering, cross-validation and model comparison.
- Integrate authorised log sources and a dashboard only after suitable testing and privacy review.
- Do not use this prototype alone to make security or incident-response decisions.

## Academic project note

This repository is a reproducible demonstration scaffold for the project title **Cyber Hacking Breach Modelling and Prediction**. Update this README to describe the exact dataset, algorithms, modules, tools and implementation that you personally used in your final-year project. Do not claim that this sample implementation is identical to your original college project unless it is.
