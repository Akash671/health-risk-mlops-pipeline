---
title: Health Risk MLOps Pipeline
emoji: 🏥
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
pinned: false
---

# Automated Patient Health Risk Prediction Pipeline

An enterprise-grade production MLOps system featuring **Continuous Integration (CI)**, **Continuous Deployment (CD)**, and **Continuous Training (CT)**.

## Architecture Ecosystem
* **Data Layer:** Supabase Cloud PostgreSQL
* **Engine Pipeline Runtime:** Docker via Python 3.10
* **Deployment Serving Target:** Hugging Face Spaces (FastAPI Web Service)
* **Automation Workflow Engine:** GitHub Actions Scheduler (Monthly Retraining Run)
