import pandas as pd
import numpy as np
REQUIRED_COLUMNS = ["Reservation_ID", "Facility_Type", "Lead_Time_Days", "Day_Of_Week", "User_Category", "Participants", "Usage_Status", "Actual_Attendance"]
FEATURE_COLUMNS = ["Lead_Time_Days", "Participants", "Facility_Type", "User_Category"]
RAW_DATA = {
"Reservation_ID": [101,102,103,104,105,106,107,108,109,110,110,111,112,113,114,115],
"Facility_Type": ["study room","Conference Hall","Auditorium","STUDY ROOM",None,"Conference Hall","Study Room","Auditorium","Conference Hall","Study Room","Study Room","Conference Hall","Study Room","Auditorium","Study Room","Conference Hall"],
"Lead_Time_Days": [1,15,5,0,12,22,2,-1,4,8,8,1,18,3,0,10],
"Day_Of_Week": ["Monday","Friday","Wednesday","Tuesday","Thursday","Monday","Saturday","Sunday","Wednesday","Friday","Friday","Monday","Wednesday","Thursday","Tuesday","Friday"],
"User_Category": ["student","Faculty","Student","EXTERNAL","Student","Faculty","student","Staff","Student","faculty","faculty","student","Student","Faculty","student","Staff"],
"Participants": [4,25,100,2,None,15,6,80,5,10,10,8,4,50,2,20],
"Usage_Status": ["Used","Cancelled","Used","No-Show","Used","Cancelled","No-Show","Used","Used","Used","Used","No-Show","Cancelled","Used","No-Show","Used"],
"Actual_Attendance": [4,0,95,0,8,0,0,75,5,10,10,0,0,48,0,18]}

def sample_data():
    return pd.DataFrame(RAW_DATA)

def clean_data(df):
    df=df.copy()
    if "Participants" in df: df["Participants"]=pd.to_numeric(df["Participants"],errors="coerce"); df["Participants"]=df["Participants"].fillna(df["Participants"].median())
    if "Facility_Type" in df: df["Facility_Type"]=df["Facility_Type"].fillna("Unknown").astype(str).str.strip().str.title()
    if "User_Category" in df: df["User_Category"]=df["User_Category"].fillna("Unknown").astype(str).str.strip().str.title()
    if "Lead_Time_Days" in df: df["Lead_Time_Days"]=pd.to_numeric(df["Lead_Time_Days"],errors="coerce")
    if "Actual_Attendance" in df: df["Actual_Attendance"]=pd.to_numeric(df["Actual_Attendance"],errors="coerce")
    df=df.drop_duplicates()
    if "Participants" in df and "Lead_Time_Days" in df: df=df[(df["Participants"]>0)&(df["Lead_Time_Days"]>=0)].copy()
    if "Lead_Time_Days" in df: df["Lead_Time_Category"]=df["Lead_Time_Days"].apply(lambda x: "Last Minute" if x<=2 else "Short Lead" if x<=7 else "Medium Lead" if x<=14 else "Early Booking")
    if "Usage_Status" in df: df["Reservation_Outcome"]=df["Usage_Status"].apply(lambda x: "Completed" if str(x).strip().title()=="Used" else "Not Completed")
    if "Participants" in df and "Actual_Attendance" in df: df["Attendance_Ratio"]=np.where(df["Participants"]>0,df["Actual_Attendance"]/df["Participants"],np.nan)
    return df

def validate_columns(df):
    return [c for c in REQUIRED_COLUMNS if c not in df.columns]
