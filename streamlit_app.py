import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
APP_TITLE = "Travel Vista Platform Dashboard"

st.set_page_config(page_title=APP_TITLE, layout="wide")
st.markdown('''
<style>
.block-container {padding-top: 1.5rem; padding-bottom: 2rem; max-width: 1180px;}
[data-testid="stMetricValue"] {font-size: 1.65rem;}
.small-note {color: #5f6368; font-size: 0.92rem;}
</style>
''', unsafe_allow_html=True)


def load(name):
    p = Path("data") / name
    return pd.read_csv(p) if p.exists() else pd.DataFrame()

dest = load("destinations.csv")
reviews = load("reviews.csv")
visits = load("visit_counts.csv")
logs = load("activity_logs.csv")
st.title(APP_TITLE)
st.caption("Capstone dashboard for travel destinations, engagement, reviews, and platform activity.")
cols = st.columns(4)
cols[0].metric("Destinations", len(dest))
cols[1].metric("Reviews", len(reviews))
cols[2].metric("Visit records", len(visits))
cols[3].metric("Activity logs", len(logs))
if not dest.empty:
    st.subheader("Destination catalog")
    st.dataframe(dest.head(50), use_container_width=True, hide_index=True)
if not reviews.empty:
    num = reviews.select_dtypes("number")
    if not num.empty:
        st.plotly_chart(px.histogram(reviews, x=num.columns[0]), use_container_width=True)
if not visits.empty:
    st.subheader("Visit-count sample")
    st.dataframe(visits.head(50), use_container_width=True, hide_index=True)
st.subheader("Architecture")
st.markdown("Flask API + OAuth/TLS concepts + PostgreSQL/MongoDB storage + Kafka/Spark-style processing + AWS S3 media layer")
