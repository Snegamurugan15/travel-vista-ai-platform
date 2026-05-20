
import streamlit as st
import pandas as pd
import joblib

# Load the full pipeline model
model = joblib.load("vr_engagement_model.pkl")

st.set_page_config(page_title="VR Engagement Predictor", layout="centered")
st.title("🧠 VR Engagement Predictor for Travel Vista")

st.markdown("Use this tool to predict whether a user will engage with VR travel packages based on their preferences.")

# User input fields
age_group = st.selectbox("Age Group", ["18-25", "26-35", "36-50", "51+"])
travel_freq = st.selectbox("Travel Frequency", ["Rarely", "Occasionally", "Frequently"])
interest_vr = st.slider("Interest in VR (1 = Low, 5 = High)", 1, 5, 3)
experience_rating = st.slider("Previous Travel Experience Rating", 1, 10, 5)
package_type = st.selectbox("Package Type", ["Economy", "Standard", "Premium", "Luxury"])
duration = st.slider("Duration of Trip (Days)", 5, 14, 7)
price = st.number_input("Package Price (USD)", value=1500.00)

# Make prediction
if st.button("Predict VR Engagement"):
    input_df = pd.DataFrame([{
        "Age_Group": age_group,
        "Travel_Frequency": travel_freq,
        "Interest_in_VR": interest_vr,
        "Past_Experience_Rating": experience_rating,
        "Package_Type": package_type,
        "Duration_Days": duration,
        "Price_USD": price
    }])
    
    prediction = model.predict(input_df)[0]
    
    if prediction:
        st.success("✅ This user is likely to engage with VR packages!")
    else:
        st.warning("❌ This user may not engage with VR packages.")

st.markdown("---")
st.caption("Built as part of the WIL Travel Vista VR Integration Project")
