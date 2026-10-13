# ICT Helpdesk Ticket Resolver (Django + Keras MIMO)

An intelligent IT support ticketing system that leverages a Multi-Input Multi-Output (MIMO) Keras deep learning model to automatically categorize, prioritize, or predict resolution paths for incoming IT incidents based on historical dataset records.

---

## Features
- **Automated Ticket Classification:** Predicts multiple attributes simultaneously (e.g., category, priority, and assigned team) using a Keras MIMO architecture.
- **Django Web Interface:** Seamlessly submit new ICT tickets and view real-time model predictions.
- **Reproducible Training Pipeline:** Includes a Jupyter notebook (`training_pipeline.ipynb`) trained on historical incident logs.

---

## Project Structure
- `ticketing_app/`: Core Django application handling views, forms, and database models.
- `it_project/`: Project-level configurations and URL routings.
- `it_mimo_model.keras`: Saved pre-trained Keras MIMO model.
- `training_pipeline.ipynb`: Data preprocessing and model training script.

---

## Getting Started

### 1. Clone the Repository & Setup Virtual Environment
```bash
git clone [https://github.com/your-username/it_mimo_django.git](https://github.com/your-username/it_mimo_django.git)
cd it_mimo_django
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
💡 Architecture & Best Practice Recommendations for Keras MIMO in Django

1. **Model Loading Singleton / Lazy Loading:** 
   Avoid loading your `it_mimo_model.keras` file inside view functions on every HTTP request, as model loading is heavy and introduces massive latency. Instead, load the model once inside `ticketing_app/apps.py` (inside the `ready()` method) or handle it as a cached singleton service inside a dedicated `services.py` module.
   
2. **Preprocessing Pipeline Consistency:**
   Ensure that whatever tokenizers, label encoders, or scalers (`StandardScaler`, `CountVectorizer`, etc.) you used during training in `training_pipeline.ipynb` are saved (e.g., using `pickle` or `joblib`) and loaded alongside the model during inference. Incoming ticket text fields must undergo the exact same cleaning pipeline before being passed into the Keras model.

3. **Database Integration:**
   Store incoming tickets using Django models (`models.Model`) capturing input text/features alongside the model's output prediction logits/probabilities. This creates a feedback loop for future model auditing and retraining.