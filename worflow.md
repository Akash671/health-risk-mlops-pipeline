# Enterprise MLOps Project: Patient Health Risk Stratification

This document details the project framework, standard operational workflow, and future challenges for the Patient Health Risk Prediction Pipeline. This structure follows the STAR method format commonly used in technical and behavioral interviews.

---

## 1. Problem Statement

Healthcare providers and health-tech startups struggle to identify high-risk patients before serious illness occurs. Manual charts and questionnaire reviews are:
* **Slow and expensive**: Clinicians cannot review every patient file manually at scale.
* **Prone to human bias**: Different staff use varying criteria to estimate patient risk.
* **Prone to model decay**: Static machine learning models built in local notebooks fail to adapt as incoming patient demographics, lifestyles, or data distributions change.

---

## 2. Task

As the AI/ML Engineer, the task was to design, implement, and deploy an end-to-end, production-ready MLOps system that:
* Ingests survey-based patient inputs (lifestyle, stress, demographics, and clinical history).
* Standardizes data preprocessing and training steps in a leakage-free pipeline.
* Deploys a multi-class classification model (Low / Medium / High Risk) as a high-availability REST API.
* Establishes automated CI/CD and Continuous Training (CT) schedules to prevent performance degradation.

---

## 3. Action / MLOps Workflow

The project is structured into three execution phases aligned with enterprise MLOps standards:

### Phase 1: Data & Model Development (ML Pipeline)
1. **Data Engineering**: Fetch raw patient records from databases (e.g., PostgreSQL / BigQuery / RDS) and load them into processing environments.
2. **Feature Engineering**: Perform Exploratory Data Analysis (EDA), handle missing values, and clip outliers using the 1.5 × IQR rule.
3. **Data Splitting**: Split data into Train, Validation, and Test sets **before** applying transformations to guarantee zero data leakage.
4. **Preprocessing Transformations**: Fit scalers and categorical encoders (e.g., `StandardScaler`, `OneHotEncoder`) *only* on the training dataset. Transform the validation and test datasets using these fitted objects.
5. **Model Training & Tuning**: Train a Random Forest classifier with `class_weight='balanced'` to offset class imbalance, tuning hyperparameters using validation sets.
6. **Model Evaluation**: Verify metrics (Recall for High Risk, Precision, F1-Score, and ROC-AUC) on the clean test set.

### Phase 2: Serialization, Packaging & Inference
7. **Model Serialization**: Bundle the preprocessing step and the trained classifier into a single pipeline object (e.g., scikit-learn `Pipeline`) and serialize it.
8. **Artifact Upload**: Save the versioned pipeline artifact (`model.joblib`) to cloud storage (GCS or S3).
9. **Model Registry**: Register the artifact in a central model registry (Vertex AI Model Registry / SageMaker Model Registry) to track production vs. candidate versions.
10. **API Wrapping**: Build a REST API using **FastAPI** and **Pydantic** to receive incoming JSON patient payloads and return risk scores.
11. **Containerization**: Write a standard `Dockerfile` that packages dependencies, code, and the serialization loader into a portable image.

### Phase 3: Deployment & MLOps Governance
12. **CI/CD/CT Automation**: Set up build pipelines (GitHub Actions / GCP Cloud Build / AWS CodePipeline) to run unit tests (`pytest`) on code changes.
13. **Container Registry**: Build and push the Docker image to a secure registry (Google Artifact Registry / Amazon ECR).
14. **Production Deployment**: Deploy the container to serverless runtimes (Google Cloud Run / AWS ECS Fargate) to serve predictions over secure HTTPS endpoints.
15. **Production Monitoring**: Log incoming features and predictions (Cloud Logging / CloudWatch) to track inference latency and error rates.
16. **Continuous Training (CT)**: Orchestrate a monthly schedule using serverless schedulers to trigger the pipeline, fetch fresh patient labels, retrain, and redeploy.

---

## 4. Result & Business Impact

* **100% Automated Lifecycle**: Mitigated technical debt by automating the model training, testing, containerization, and deployment stages.
* **Clinical Safety**: Optimized the classifier's recall on High-Risk cases, ensuring patients requiring immediate attention are flagged while reducing false-alarm "alert fatigue" for coordinators.
* **Low Latency & High Scale**: Achieved sub-second response times, enabling clinical portals or mobile applications to query risk metrics instantaneously.
* **Compliance Ready**: Isolated infrastructure credentials from code using secrets mounting at container build time, meeting key enterprise security criteria.

---

## 5. Challenges to Face in the Future

As this system scales to support millions of active patients in a corporate setting, several engineering and compliance challenges will arise:

### A. HIPAA Compliance & PHI Security
* **Challenge**: Patient lifestyle and medical inputs represent Protected Health Information (PHI). Storing raw telemetry in standard logs or passing unencrypted payloads violates privacy standards.
* **Solution**: Implement tokenization/masking proxy servers to strip personal identifiers (names, SSNs) before they reach the ML model. Ensure encryption keys (KMS) are managed under strict IAM permissions.

### B. Severe Data and Concept Drift
* **Challenge**: Over time, patient behaviors change (e.g., sudden shifts in sleep/activity patterns during public health crises or seasonal changes), leading to drop-offs in prediction quality.
* **Solution**: Deploy continuous drift-detection monitors (Vertex AI Model Monitor / SageMaker Model Monitor) comparing baseline training feature distributions against real-time API logs, triggering slack/alert webhooks when drift threshold is exceeded.

### C. Data Validation at the Ingestion Gate
* **Challenge**: Telehealth apps or doctors may enter invalid, corrupted, or null data (e.g., negative ages, BMIs over 100), causing prediction errors.
* **Solution**: Introduce a strict data validation layer (e.g., **Great Expectations** or **Pydantic** strict validation) at the ETL ingress gate to isolate anomalous records in a quarantine table for review.

### D. Cold Start Latency in Serverless Environments
* **Challenge**: If deployed on Cloud Run or AWS Lambda to optimize costs, scale-from-zero behavior can cause the first clinical request to take several seconds while loading the container and model dependencies.
* **Solution**: Set a minimum container instance limit (e.g., `min-instances=1`) in Cloud Run/ECS config to keep a container warm, or use memory-cached model loaders.
