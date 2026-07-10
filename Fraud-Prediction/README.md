# Credit Card Fraud Detection using Machine Learning

A machine learning project that predicts whether a credit card transaction is fraudulent using anonymized transaction features. This project demonstrates a complete machine learning workflow, from data preprocessing and feature engineering to model selection, hyperparameter tuning, and performance evaluation on an imbalanced classification problem.

---

## Project Overview

Credit card fraud represents a significant challenge for financial institutions due to the rarity of fraudulent transactions and the high financial cost of missed detections.

This project develops a fraud detection model capable of identifying suspicious transactions using historical transaction data. Because fraudulent transactions account for less than 1% of all observations, special attention is given to model evaluation metrics that balance fraud detection performance with false alarm rates.

---

## Dataset

The project is based on the **Credit Card Fraud Detection** dataset, originally published on Kaggle.

The dataset contains anonymized credit card transactions collected over a two-day period.

### Features

- **PC01 – PC28**
  - Principal components generated through PCA to preserve customer privacy

- **Amount**
  - Transaction amount (USD)

### Target

- **Fraud**
  - 0 = Legitimate transaction
  - 1 = Fraudulent transaction

### Dataset Statistics

| Metric | Value |
|---------|------:|
| Training Samples | 54,276 |
| Features | 29 |
| Fraud Rate | 0.58% |

The notebook automatically downloads both the training and testing datasets.

---

## Machine Learning Pipeline

### Data Preprocessing

- Mean imputation for missing values
- Standardization using `StandardScaler`
- Pipeline implementation with `ColumnTransformer`

### Model

- Decision Tree Classifier

### Hyperparameter Tuning

Grid Search Cross Validation was used to optimize:

- Maximum tree depth
- Random state
- Class weights

The model was optimized using **F₂ Score**, which places greater emphasis on **Recall**, an important metric in fraud detection where missing fraudulent transactions is particularly costly.

---

## Model Evaluation

Performance was evaluated using:

- Precision
- Recall
- F₂ Score (during model selection)
- Confusion Matrix

---

## Results

### Test Performance

| Metric | Score |
|--------|-------:|
| Precision | **0.929** |
| Recall | **0.823** |

The model successfully identified over **82% of fraudulent transactions** while maintaining a **92.9% precision**, indicating a low false-positive rate.

---

## Key Insights

- Successfully handled an extremely imbalanced dataset where fraud represented only **0.58%** of transactions.
- Optimized model performance using class weighting and cross-validation.
- Demonstrated the importance of selecting evaluation metrics beyond overall accuracy when working with rare-event classification problems.

---

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/Projects-and-Coursework.git

cd Projects-and-Coursework/Credit-Card-Fraud-Detection
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Project

Launch Jupyter Notebook:

```bash
jupyter notebook
```

or

```bash
jupyter lab
```

The notebook downloads the training and testing datasets automatically.

---

## Tools Used

- Python
- NumPy
- Pandas
- Scikit-learn
- Matplotlib
- Seaborn
- Jupyter Notebook
