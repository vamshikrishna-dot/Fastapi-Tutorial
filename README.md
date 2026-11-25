# Patient Management System

A FastAPI app to create, view, update and delete patient records, with automatic BMI and health verdict calculation. Data is stored in `patients.json`.

## Run locally

```bash
python -m venv myenv
myenv\Scripts\activate        # Windows  (Linux/Mac: source myenv/bin/activate)
pip install -r requirements.txt
uvicorn main:app --reload
```

Open http://127.0.0.1:8000/docs for the interactive API docs.
