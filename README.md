# Projects and Coursework

A collection of data science and machine learning projects completed as part of my coursework at the **University of Illinois**.

Each project follows a full data science workflow — from data cleaning and exploratory analysis to model tuning and evaluation — applied to a real, publicly available dataset.

## Topics Covered

- Data Cleaning & Preprocessing
- Exploratory Data Analysis (EDA)
- Data Visualization
- Linear Regression
- Classification
- Decision Trees
- K-Nearest Neighbors
- Model Evaluation & Hyperparameter Tuning

## Projects

| Project | Description | Techniques | Result |
|---|---|---|---|
| [**Credit Card Fraud Detection**](./Fraud-Prediction) | Detects fraudulent credit card transactions in a highly imbalanced dataset (0.58% fraud rate) using anonymized, PCA-transformed features. | Decision Tree Classifier, GridSearchCV, F₂ Score optimization | 92.9% precision, 82.3% recall |
| [**Wine Quality Prediction**](./Wine-Quality-Prediction) | Predicts the quality score of Portuguese *Vinho Verde* wines from their chemical properties, replacing subjective sommelier tasting with a data-driven model. | K-Nearest Neighbors, GridSearchCV, one-hot encoding | 0.476 Mean Absolute Error |

Each project folder contains its own `README.md` with full details on the dataset, methodology, and results, plus a `Report.ipynb`/`Report.html` walkthrough and the underlying `Model.ipynb`.

## Repository Structure

```
Projects-and-Coursework/
├── Fraud-Prediction/
│   ├── Model.ipynb          # Model development notebook
│   ├── Report.ipynb          # Full write-up / analysis
│   ├── Report.html           # Rendered report
│   ├── requirements.txt
│   └── README.md
├── Wine-Quality-Prediction/
│   ├── Model2.ipynb
│   ├── Report.ipynb
│   ├── Report.html
│   ├── requirements.txt
│   └── README.md
└── README.md                 # You are here
```

## Getting Started

Clone the repository:

```bash
git clone https://github.com/HarlowNg/Projects-and-Coursework.git
cd Projects-and-Coursework
```

Each project is self-contained with its own dependencies. To run a specific project, `cd` into its folder and install its requirements:

```bash
cd Fraud-Prediction        # or Wine-Quality-Prediction
pip install -r requirements.txt
jupyter notebook
```

Datasets are downloaded automatically by the notebooks — no manual download needed.

## Tools 

- **Language:** Python
- **Libraries:** NumPy, Pandas, Scikit-learn, Matplotlib, Seaborn, PyArrow
- **Environment:** Jupyter Notebook / JupyterLab

## About

These projects were built to demonstrate practical, end-to-end machine learning skills, including handling imbalanced data, tuning models with cross-validation, and choosing evaluation metrics appropriate to the problem.
