import pandas as pd
def build_review_queue(df, bundle):
    from modules.prediction import predict_one
    rows=[]
    for _,r in df.iterrows():
        try:
            pred,probs=predict_one(bundle,r["Lead_Time_Days"],r["Participants"],r["Facility_Type"],r["User_Category"])
            rows.append({"Reservation_ID":r.get("Reservation_ID","—"),"Facility_Type":r["Facility_Type"],"Lead_Time_Days":r["Lead_Time_Days"],"Participants":r["Participants"],"Predicted_Outcome":pred,"Model_Confidence":max(probs.values()) if probs else None,"Review_Status":"Needs human review" if pred=="Not Completed" else "Routine review"})
        except Exception: continue
    return pd.DataFrame(rows)
