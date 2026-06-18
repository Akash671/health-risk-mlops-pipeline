# Automated Patient Health Risk Prediction Pipeline

An enterprise-grade production MLOps system featuring **Continuous Integration (CI)**, **Continuous Deployment (CD)**, and **Continuous Training (CT)**.

## Architecture Ecosystem
* **Data Layer:** Supabase Cloud PostgreSQL
* **Engine Pipeline Runtime:** Docker via Python 3.10
* **Deployment Serving Target:** Hugging Face Spaces (FastAPI Web Service)
* **Automation Workflow Engine:** GitHub Actions Scheduler (Monthly Retraining Run)

## Production Deployment Steps
1. Fork or clone this repository structure.
2. Add repository secrets in GitHub Settings:
   * `SUPABASE_DB_URL`
   * `HF_TOKEN`
3. Commit updates to the main branch to automatically trigger the end-to-end pipeline.



https://www.google.com/search?q=Chronic+Disease+History%09Stress+Level+%281-10%29%0A840%0926%09Other%0924.06%09Never%0916%096.8%096.1%09Hypertension%092%0A550%0978%09Male%0929.19%09Current%099%0910.0%099.1%09Heart+Disease%092%0A351%0940%09Female%0921.44%09Never%0912%093.9%098.3%09Heart+Disease%092%0A203%0956%09Female%0927.24%09Current%0914%093.4%096.8%09Diabetes%092%0A193%0949%09Other%0931.49%09Never%099%096.6%097.5%09Heart+Disease%09%0A%0A%0A%23%23+how+to+fill+misign+values+here%3F&sourceid=chrome&ie=UTF-8&aep=48&cud=0&qsubts=1781615259103&source=chrome.crn.obic&mstk=AUtExfBpXSi9Vph_LmGf1vcLQ7QkYcs5DLlYznX1MbUYXJLTC2mQZmhr9uCoDtuD-GBFgUnCclF81JLQNTVoTcxQwV39CHD3z3QZdrCooM4YDwdoGu-O94ZQW9HgRBsyCnsJir5M8ugu-OMcaKvYFk5npFSWv0lx3GvNTHXToQ1gW9WSK_N3tkDBzEWCAEjo90RZUYSeB4ltUauxwGaA3b4Ns0yu6j2xcP5BGmswB5ldJti4GHDxEvlAXinO8gq21wAO9_iX819WWnIttpoDe-vEzzWThDNdv2tpEFx6kG2CsSYaOKMVL-Tl4EZ7KeI-9tQaq_tVRKNXKJZv0g&csuir=1&mtid=yUoxatGiFvfmi-gPhNnTuAE&lns_mode=cvst&udm=50