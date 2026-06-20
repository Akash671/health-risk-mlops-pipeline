workflow:



# expeiments and developement
1. data engineering (data gathering, data pipeline and data processng pipeline)
2. feature engineering+data analysis
3. data splitting (train, test, validataion) + also prevvent data leakge 
4. model traning & expeerimets and ovservation , hyper parameter tuning, analyzing overfitting and underfitting
5. appltying regularization methods 
5. evvalution metrics (recall, precession, F1-score, MSE, RMSE etc.)
6. saved bset model in pytorch/tensoflow/pkl foramt

# production and deployment
1. data piplein + cloud database (GCP cloud storeage , AWS S3 bucket etc)
2. model traniing pipeline, pytest etc.
3. model registry in GCS rigstry/AWS registry
4. application wraped with fastapi backend 
5. created dockerfile with required instruction, requiremtn.txt file
6. crated CI/CD/CT automated configuration workflow pipline file(github/action/yaml file)
7. code pushed on github repo/GCS Repo/AWS repo/Azure repo
8. CI/CD/CT piplien trigger 
9. Docker file create docker image then
10. then image run as container on cloud service hugginface/GCP cloud run/GCP vertexai endpoeint / AWS Cloud/Azure Cloud
11. application live for users
12. performace moniorting + alertring when performace degrading or data drift observe
13. re-train every month, evaluatrin old and new version of model usign A/B testing 
=================================================================================================

🔬 Phase 1: Experiments & Development

1. Data Engineering
Data gathering/acquisition from various sources.Data pipeline creation (ingesting raw data streams into intermediate storage).

Data processing pipeline (handling missing values, anomalies, and basic type casting).

2. Feature Engineering & Data Analysis Exploratory Data Analysis (EDA) to find correlations, target imbalances, and skewness.Feature engineering (creating interactions, handling text/categorical encoding, numeric scaling).Correction: Feature selection (dropping low-importance columns using trees or statistical scores).

3. Data Splitting & Leakage PreventionCorrection: Split your data into Train, Validation, and Test sets BEFORE applying imputation, scaling, or encoding.Critical Enterprise Rule: Calculate all preprocessing parameters (e.g., mean, median, mode, one-hot categories) strictly from the Training set. Apply those saved parameters to the Validation and Test sets to prevent severe Data Leakage.

4. Model Training, Experiments & ObservationBaseline training across multiple model architectures (Linear, Tree-based, Boosting).Hyperparameter tuning (GridSearchCV, RandomizedSearchCV, or Optuna).Analyzing training vs. validation curves to spot Overfitting (high train score, low val score) and Underfitting (low train score, low val score).

5. Applying Regularization MethodsLinear models: L1 (Lasso), L2 (Ridge), ElasticNet.Tree-based models: Limiting max_depth, increasing min_samples_leaf, or applying L1/L2 weights in XGBoost.Deep Learning: Dropout layers, Batch Normalisation, Early Stopping.

6. Evaluation MetricsCorrection: Separate your metrics by task type! You mixed classification and regression together:Classification Tasks: Recall, Precision, F1-Score, ROC-AUC, LogLoss.Regression Tasks: MSE (Mean Squared Error), RMSE, MAE (Mean Absolute Error), \(R^{2}\) Score.

7. Saving the Best ModelExporting model objects and weights: PyTorch (.pt), TensorFlow SavedModel format, or Scikit-Learn binaries (.pkl, .joblib).Best Practice Addition: Export your preprocessing states (e.g., your Scaler and Encoder) alongside the model so the production API can handle raw input text identically.


🚀 Phase 2: Production & Deployment

1. Data Pipeline + Cloud DatabaseRaw data ingested into a secure cloud store (AWS S3, Google Cloud Storage, Azure Blob Storage) or database (PostgreSQL/Supabase, Snowflake, BigQuery).

2. Model Training Pipeline & TestingAutomated reproducible training script (train.py).Integration Testing (pytest): Runs automated test cases verifying API endpoints, column types, and database connectivity.

3. Model RegistryCorrection: Use a dedicated model management tool (MLflow Model Registry, GCP Vertex AI Model Registry, or AWS SageMaker Model Registry). Standard storage buckets (GCS/S3) are ok for backups, but real registries handle explicit version control (e.g., Staging vs. Production flags).

4. Application FrameworkWrapping the inference logic with a production asynchronous gateway (FastAPI with Uvicorn worker threads).

5. Containerization FilesCreating a multi-stage Dockerfile to build an image container footprint, combined with a strict requirements.txt locking down all version dependencies.

6. CI/CD/CT ConfigurationCreating configuration workflow scripts (GitHub Actions .yml, GitLab CI, Jenkins, or AWS CodePipeline).

7. Remote Code ManagementPushing code to a secure repository host (GitHub, GitLab, AWS CodeCommit, Azure Repos).

8. CI/CD/CT Pipeline TriggerAutomated build launches upon code updates to the main branch or via an automated chronological schedule.

9. Container Image ManagementCorrection: The runner creates the Docker image, but it must be pushed to a Container Registry (Docker Hub, AWS ECR, GCP Artifact Registry) before it can deploy to production.

10. Container Deployment RunThe cloud service pulls the image from the registry and mounts it to an active node (Hugging Face Spaces, GCP Cloud Run, Vertex AI Endpoint, AWS ECS/App Runner).

11. Live ServingThe application goes live, exposing secure endpoints (/predict, /health) to your end-users.

12. Monitoring & AlertingContinuous performance monitoring tracking runtime performance (Latency, Errors) and statistical metrics (Data Drift, Concept Drift via EvidentlyAI or Great Expectations). Alerts trigger email/Slack flags if accuracy metrics decay.

13. Automated Continuous Training (CT) & Release ValidationAutomated retraining cycle runs on a schedule (e.g., every month) combining historical data with newly captured production inputs.Correction: Instead of jumping straight into A/B testing on live users, perform Shadow Deployments or Champion vs. Challenger evaluation on a validation split. If the new model beats the old model, route traffic using an A/B distribution channel.
==================================================================================================


## 🗺️ Enterprise Cloud Architecture Mapping

The table below maps the current experimental pipeline setup to enterprise-grade production services on **Google Cloud Platform (GCP)** and **Amazon Web Services (AWS)**:

| Component Layer | Current Experimental Setup | Google Cloud (GCP) Match | Amazon Web Services (AWS) Match |
| **1. Source Control** | GitHub | GitHub / Cloud Source Repositories | GitHub / AWS CodeCommit |
| **2. CI/CD/CT Automation** | GitHub Actions | Cloud Build / Vertex Pipelines | AWS CodePipeline / SageMaker Pipelines |
| **3. Container Storage** | Hugging Face Git Repository | Artifact Registry | Elastic Container Registry (ECR) |
| **4. Serverless Hosting** | Hugging Face Spaces | **Cloud Run** | **AWS App Runner** / ECS Fargate |
| **5. Core Model Registry** | Local `model.pkl` Binary | Vertex AI Model Registry | SageMaker Model Registry |
| **6. Secret Storage** | Hugging Face Space Secrets | Secret Manager | AWS Secrets Manager |
| **7. Production Database** | Supabase Cloud (PostgreSQL) | Cloud SQL (PostgreSQL) | Amazon RDS (PostgreSQL) / Aurora |











### database bucket of store live stream data: 
https://supabase.com/dashboard/project/nevzmprqlpxjmgvbvkhh/database/tables



### main.py file

is for model running testing



### future enhancements

1. scalling
2. batch processing
3. performance monitoring 
4. alertring 


