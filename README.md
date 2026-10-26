# Facility Reservation Insights — Streamlit

A Streamlit decision-support app adapted from the uploaded midterm Python file for campus/library facility reservations.

## Run locally

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Pages
- Home
- Dataset upload, schema validation, cleaning summary, and CSV export
- Data Analysis with interactive charts
- Prediction from lead time, participants, facility type, and user category
- Dashboard and human-review queue
- System Design and SAD requirements

## Important model provenance note
The uploaded midterm script trains `DecisionTreeClassifier(max_depth=3, random_state=42)` on `Lead_Time_Days`, `Participants`, `Facility_Type`, and `User_Category`, with target `Reservation_Outcome`. It does not save a fitted model artifact. Therefore, `models/trained_model.joblib` is reconstructed from the example dataset embedded in that script using the same feature set and classifier settings. Replace it with the actual saved midterm model if available, and verify predictions against the original notebook before submission. The included dataset is tiny and appears illustrative; do not treat its metrics or predictions as production quality.

## Deploy
Push this folder to a GitHub repository. In Streamlit Community Cloud, create an app from the repository and select `app.py` as the entry point.

## Privacy and decision use
Use synthetic or properly authorized data. Predictions support staff review and must not automatically reject reservations or deny services.
