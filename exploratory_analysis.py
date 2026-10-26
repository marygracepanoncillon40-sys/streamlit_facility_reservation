import plotly.express as px
def facility_chart(df): return px.bar(df["Facility_Type"].value_counts().rename_axis("Facility Type").reset_index(name="Reservations"),x="Facility Type",y="Reservations",title="Reservations by Facility Type")
def outcome_chart(df): return px.pie(df,names="Reservation_Outcome",title="Reservation Outcome Distribution",hole=.35)
def lead_chart(df): return px.histogram(df,x="Lead_Time_Category",color="Reservation_Outcome",barmode="group",category_orders={"Lead_Time_Category":["Last Minute","Short Lead","Medium Lead","Early Booking"]},title="Outcomes by Lead-Time Category")
def category_chart(df): return px.bar(df,x="User_Category",color="Reservation_Outcome",barmode="group",title="Outcome by User Category")
