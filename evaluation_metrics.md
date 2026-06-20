# Model Evaluation Metrics & Production Benchmarks

This document details the evaluation metrics, baseline expectations, and production-grade targets for the **Patient Health Risk Prediction Pipeline**. In healthcare risk stratification (Low / Medium / High classification), relying solely on standard accuracy can lead to dangerous clinical outcomes due to class imbalance.

---

## 1. Core Evaluation Metrics

Rather than tracking a single global accuracy score, the system is evaluated using a combination of metrics tailored for imbalanced classification:

| Metric | Formula / Concept | Clinical & Business Meaning |
| :--- | :--- | :--- |
| **Accuracy** | $\frac{TP + TN}{TP + TN + FP + FN}$ | The overall proportion of correct classifications. Use with caution due to class imbalance. |
| **Recall (Sensitivity)** | $\frac{TP}{TP + FN}$ | **Crucial for High Risk.** The proportion of actual high-risk patients correctly identified. High recall ensures fewer at-risk patients are missed (low False Negatives). |
| **Precision** | $\frac{TP}{TP + FP}$ | **Crucial for Operations.** Out of all patients flagged as high-risk, how many actually are? High precision reduces alert fatigue and optimizes clinician resource allocation (low False Positives). |
| **F1-Score** | $2 \times \frac{Precision \times Recall}{Precision + Recall}$ | The harmonic mean of Precision and Recall. Highly useful for evaluating the minority classes (Medium and High Risk). |
| **ROC-AUC** | Area under the True Positive Rate vs. False Positive Rate curve | Measures the model's ability to distinguish between classes across all possible classification thresholds. |

---

## 2. Production Performance Targets

When deploying a model to production on GCP or AWS, the following performance tiers define the release criteria:

### 📊 Performance Tiers Table

| Performance Level | Target Accuracy / F1-Score | Target ROC-AUC | Release Status / Action |
| :--- | :--- | :--- | :--- |
| **Below Baseline** | < 65% Accuracy / F1 | < 0.70 | **DO NOT DEPLOY.** The model is performing near random chance or simple heuristics. |
| **Minimum Acceptable (Floor)** | 65% – 75% | 0.70 – 0.78 | **Deployable for Triage Support.** Good enough to act as an automated secondary check or to filter low-risk cases. |
| **Target Production Goal** | **75% – 85%** | **0.80 – 0.88** | **Standard Production Release.** Optimal balance between recall (catching sick patients) and precision (preventing clinical alert fatigue). |
| **High Performance** | 85% – 92% | 0.88 – 0.94 | **Premium Model.** Achieved when combining vitals/lab data with everyday lifestyle surveys. |
| **Suspiciously High (Red Flag)** | > 93% | > 0.95 | **Hold Release & Audit.** Almost always indicates data leakage, target contamination, or severe overfitting. |

---

## 3. Key Risks in Production Metrics

### A. Class Imbalance & The "Accuracy Paradox"
If 80% of your patient population is Low Risk, a naive model that predicts "Low Risk" for everyone gets **80% Accuracy**, yet has **0% Recall** for Medium and High-risk classes.
* **Mitigation**: Always report class-level metrics using a classification report (Precision, Recall, F1 for each class individually) rather than an overall accuracy average.

### B. Target Leakage (Data Leakage)
If your model's accuracy on the test set is near-perfect (> 95%), look for features that contain information about the target variable which would not be available at the time of inference.
* **Example**: Including features like `prescribed_risk_medication = True` or `referred_to_cardiology = True` to predict if a patient has a high cardiovascular risk.
* **Mitigation**: Ensure that features only represent data points collected *before* the risk assessment occurs.

### C. Train-Serve Skew
If the training dataset is preprocessed as a single block (e.g., using fit-transform on the entire dataset including test splits), information leaks from the test split to the training split, artificially inflating accuracy during evaluation.
* **Mitigation**: Fit all preprocessing steps (imputers, scalers, encoders) *only* on the training split, and save the fitted transformations to apply to the test set and production payloads.
