import streamlit as st
import pandas as pd
import plotly.express as px
from modules.data_processing import sample_data, clean_data, validate_columns, REQUIRED_COLUMNS, FEATURE_COLUMNS
from modules.exploratory_analysis import facility_chart, outcome_chart, lead_chart, category_chart
from modules.prediction import load_model, predict_one
from modules.dashboard import build_review_queue

st.set_page_config(page_title="Facility Reservation Insights", page_icon="🏫", layout="wide")
st.markdown("<style>.block-container{padding-top:1.8rem}.hero{padding:1.4rem 1.6rem;border-radius:16px;background:linear-gradient(120deg,#12304a,#237a78);color:white;margin-bottom:1rem}.hero h1{color:white;margin:0}.hero p{font-size:1.05rem;margin:.45rem 0 0}</style>",unsafe_allow_html=True)
@st.cache_resource
def get_bundle(): return load_model()
@st.cache_data
def default_clean(): return clean_data(sample_data())
bundle=get_bundle()
menu=st.sidebar.radio("NAVIGATION",["Home","Dataset","Data Analysis","Prediction","Dashboard","System Design"])
st.sidebar.divider(); st.sidebar.caption("Systems Analysis and Design · Midterm project")

def get_df():
    return st.session_state.get("facility_df",default_clean())

if menu=="Home":
    st.markdown('<div class="hero"><h1>Facility Reservation Insights</h1><p>Data-driven decision support for library and campus facility reservations.</p></div>',unsafe_allow_html=True)
    data=default_clean()
    a,b,c,d=st.columns(4); a.metric("Valid records",len(data)); b.metric("Facility types",data["Facility_Type"].nunique()); c.metric("Completed",int((data["Reservation_Outcome"]=="Completed").sum())); d.metric("Not completed",int((data["Reservation_Outcome"]=="Not Completed").sum()))
    st.subheader("What this application does")
    st.write("Explore reservation data, inspect trends, estimate a reservation outcome from the midterm model features, and flag records for staff review.")
    st.info("Predictions are decision-support only. Staff must review relevant context before making any reservation decision.")
    st.markdown("**Model features:** Lead time in days, participants, facility type, and user category.")
    st.caption("The embedded sample data is the small dataset included in the submitted midterm Python file. Upload your own authorized CSV on the Dataset page.")
elif menu=="Dataset":
    st.title("Dataset Upload & Validation")
    uploaded=st.file_uploader("Upload a reservation CSV",type=["csv"])
    if uploaded is not None:
        try:
            raw=pd.read_csv(uploaded); missing=validate_columns(raw)
            if missing: st.error("Missing required columns: "+", ".join(missing)); st.caption("Expected schema: "+", ".join(REQUIRED_COLUMNS))
            else:
                st.session_state["facility_df"]=clean_data(raw); st.success("CSV loaded and cleaned successfully.")
        except Exception as e: st.error(f"Could not read this CSV: {e}")
    data=get_df(); st.subheader("Data preview"); st.dataframe(data.head(50),use_container_width=True)
    x,y,z=st.columns(3); x.metric("Rows after cleaning",len(data)); y.metric("Duplicate rows remaining",int(data.duplicated().sum())); z.metric("Missing cells",int(data.isna().sum().sum()))
    st.subheader("Missing values by column"); st.dataframe(data.isna().sum().rename("Missing values").to_frame(),use_container_width=True)
    st.download_button("Download processed CSV",data.to_csv(index=False).encode("utf-8"),file_name="processed_facility_reservations.csv",mime="text/csv")
elif menu=="Data Analysis":
    st.title("Exploratory Data Analysis")
    data=get_df()
    if data.empty: st.warning("No valid records available. Upload a valid CSV on the Dataset page.")
    else:
        with st.expander("Descriptive statistics",expanded=True): st.dataframe(data.describe(include="all").T,use_container_width=True)
        c1,c2=st.columns(2); c1.plotly_chart(facility_chart(data),use_container_width=True); c2.plotly_chart(outcome_chart(data),use_container_width=True)
        c3,c4=st.columns(2); c3.plotly_chart(lead_chart(data),use_container_width=True); c4.plotly_chart(category_chart(data),use_container_width=True)
elif menu=="Prediction":
    st.title("Reservation Outcome Prediction")
    st.write("Enter information available at the time of reservation. Do not enter actual attendance or final usage status.")
    data=get_df(); facilities=sorted(set(data.get("Facility_Type",pd.Series(dtype=str)).dropna().astype(str).tolist()+["Auditorium","Conference Hall","Study Room","Unknown"])); categories=sorted(set(data.get("User_Category",pd.Series(dtype=str)).dropna().astype(str).tolist()+["Student","Faculty","Staff","External","Unknown"]))
    with st.form("prediction_form"):
        c1,c2=st.columns(2); lead=c1.number_input("Lead time (days)",min_value=0,max_value=365,value=3); participants=c2.number_input("Number of participants",min_value=1,max_value=10000,value=10)
        c3,c4=st.columns(2); facility=c3.selectbox("Facility type",facilities); category=c4.selectbox("User category",categories)
        submit=st.form_submit_button("Predict outcome",type="primary")
    if submit:
        pred,probs=predict_one(bundle,lead,participants,facility,category)
        if pred=="Completed": st.success("Predicted outcome: Completed")
        else: st.warning("Predicted outcome: Not Completed — staff review recommended")
        if probs: st.write("Model class scores"); st.bar_chart(pd.Series(probs,name="Score"))
        st.caption("Scores are model estimates, not guarantees. The model was developed from a very small synthetic/example dataset and should not be used as the sole basis for decisions.")
elif menu=="Dashboard":
    st.title("Decision-Support Dashboard")
    data=get_df()
    if data.empty: st.warning("No valid records available.")
    else:
        queue=build_review_queue(data,bundle)
        a,b,c,d=st.columns(4); a.metric("Reservations",len(queue)); b.metric("Flagged for review",int((queue["Predicted_Outcome"]=="Not Completed").sum())); c.metric("Routine review",int((queue["Predicted_Outcome"]=="Completed").sum())); d.metric("Facilities represented",data["Facility_Type"].nunique())
        st.subheader("Human review queue")
        flagged=queue[queue["Predicted_Outcome"]=="Not Completed"]
        if flagged.empty: st.success("No records were flagged by this model in the current dataset.")
        else: st.dataframe(flagged,use_container_width=True,hide_index=True)
        with st.expander("View all scored records"): st.dataframe(queue,use_container_width=True,hide_index=True)
        st.download_button("Download review queue",queue.to_csv(index=False).encode("utf-8"),"reservation_review_queue.csv","text/csv")
        st.warning("A prediction must not automatically reject a reservation or deny services. Authorized staff make the final decision after review.")
elif menu=="System Design":
    st.title("System Design & SAD Integration")
    st.subheader("Actors")
    st.markdown("- **Facility administrator:** reviews flagged reservations and decides follow-up.\n- **Reservation staff:** maintains reservation data and checks records.\n- **Analyst / system operator:** uploads authorized CSV data and reviews model performance.\n- **Decision-support system:** validates data, analyzes trends, and produces model estimates.")
    st.subheader("Functional requirements")
    for x in ["The system shall accept CSV files and validate required columns.","The system shall show a data preview, missing values, and duplicate counts.","The system shall display descriptive statistics and interactive charts.","The system shall estimate Completed / Not Completed from the four midterm features.","The system shall provide a review queue and allow authorized staff to download results."]: st.markdown("- "+x)
    st.subheader("Non-functional requirements")
    for x in ["Usability: clear navigation and readable visualizations.","Reliability: invalid schemas and unreadable files produce actionable errors.","Privacy: use synthetic or properly authorized data; do not publish sensitive student records."]: st.markdown("- "+x)
    st.subheader("Analytical process flow")
    st.code("Authorized CSV → Schema validation → Cleaning & feature preparation → EDA → Saved model inference → Review queue → Human review and final decision",language="text")
    st.subheader("Use case overview")
    st.image("assets/use_case_diagram.png",use_container_width=True)
    st.caption("Model note: the uploaded midterm script defines a DecisionTreeClassifier(max_depth=3, random_state=42) with four features, but does not save a fitted model. The included artifact is reconstructed from the embedded dataset and the same model settings. Retrain and validate with the authoritative midterm dataset before formal use.")
