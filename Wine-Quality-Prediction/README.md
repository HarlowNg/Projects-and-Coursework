# Wine Quality Prediction using Machine Learning

A machine learning project that predicts the quality of Portuguese **Vinho Verde** wines using their chemical properties. This project demonstrates an end-to-end data science workflow including exploratory data analysis, preprocessing, model selection, hyperparameter tuning, and model evaluation.

> **Course:** CS307 – Modeling and Learning in Data Science  
> **Tools:** Python, Pandas, Scikit-learn, Matplotlib

---

## Project Overview

Traditionally, wine quality is assessed by trained sommeliers through sensory evaluation. This project explores whether measurable chemical properties can be used to predict wine quality consistently using machine learning.

The model was trained on laboratory measurements and expert quality ratings to automate the prediction process while reducing subjectivity.

---

## Dataset

The project uses the **Wine Quality Dataset** from the **UCI Machine Learning Repository**, consisting of Portuguese *Vinho Verde* wines.

Features include:

- Fixed acidity
- Volatile acidity
- Citric acid
- Residual sugar
- Chlorides
- Free sulfur dioxide
- Total sulfur dioxide
- Density
- pH
- Sulphates
- Alcohol content
- Wine color (Red / White)

Target:

- **Quality** (integer score from 0–10 assigned by expert sommeliers)

The notebook automatically downloads the training and testing datasets.

---

## Machine Learning Pipeline

The project follows a complete machine learning workflow:

- Data preprocessing
  - Missing value imputation
  - Feature scaling using `StandardScaler`
  - One-hot encoding for categorical variables

- Model development
  - K-Nearest Neighbors (KNN) Classifier

- Hyperparameter tuning
  - GridSearchCV
  - Cross-validation

- Model evaluation
  - Mean Absolute Error (MAE)
  - Confusion Matrix

---

## Results

**Test Mean Absolute Error (MAE)**

```
0.476
```

The model predicts wine quality within approximately **half a quality point** on average, demonstrating strong predictive performance using only laboratory measurements.

---


## Installation

Clone the repository and install the required packages.

```bash
git clone https://github.com/yourusername/Projects-and-Coursework.git
cd Projects-and-Coursework/Wine-Quality-Prediction

pip install -r requirements.txt
```

---

## Running the Project

Open the notebook:

```bash
jupyter notebook
```

or

```bash
jupyter lab
```

The notebook downloads the datasets automatically and reproduces the analysis.

---

## Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- Matplotlib
- Seaborn
- Jupyter Notebook
