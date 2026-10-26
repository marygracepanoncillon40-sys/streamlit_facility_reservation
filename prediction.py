import joblib
import pandas as pd
from pathlib import Path
MODEL_PATH=Path(__file__).resolve().parents[1]/"models"/"trained_model.joblib"
def load_model(): return joblib.load(MODEL_PATH)
def predict_one(bundle, lead_time_days, participants, facility_type, user_category):
    row=pd.DataFrame([{"Lead_Time_Days":float(lead_time_days),"Participants":float(participants),"Facility_Type":facility_type,"User_Category":user_category}],columns=bundle["feature_columns"])
    model=bundle["pipeline"]; pred=model.predict(row)[0]
    probs={}
    if hasattr(model,"predict_proba"):
        for label,p in zip(model.classes_,model.predict_proba(row)[0]): probs[str(label)]=float(p)
    return str(pred),probs
