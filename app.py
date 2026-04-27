import streamlit as st
import pandas as pd

st.set_page_config(page_title="SOC Dashboard", layout="wide")

st.title("SOC Security Dashboard")

df = pd.read_csv("logs.csv")

st.subheader("Security Events")
st.dataframe(df)

col1, col2, col3 = st.columns(3)

col1.metric("Total Events", len(df))
col2.metric("High/Critical Alerts", len(df[df["severity"].isin(["High", "Critical"])]))
col3.metric("Unique Source IPs", df["source_ip"].nunique())

st.subheader("Events by Severity")
severity_count = df["severity"].value_counts()
st.bar_chart(severity_count)

st.subheader("Top Source IPs")
top_ips = df["source_ip"].value_counts()
st.bar_chart(top_ips)

st.subheader("High Risk Alerts")
high_risk = df[df["severity"].isin(["High", "Critical"])]
st.dataframe(high_risk)
failed_logins = df[df["event"] == "Failed Login"]

suspicious_ips = failed_logins["source_ip"].value_counts()
suspicious_ips = suspicious_ips[suspicious_ips > 1]

st.subheader("Suspicious IP Detection")

if not suspicious_ips.empty:
    st.warning("Suspicious IPs detected based on repeated failed logins")
    st.dataframe(suspicious_ips)
else:
    st.success("No suspicious IPs detected")

st.subheader("Event Distribution")


uploaded_file = st.file_uploader("Upload Log File")


import matplotlib.pyplot as plt
st.subheader("Event Distribution")

event_counts = df["event"].value_counts()

fig, ax = plt.subplots(
    facecolor="#0A192F"
)

ax.set_facecolor("#0A192F")

ax.pie(
    event_counts,
    labels=event_counts.index,
    autopct="%1.1f%%",
    textprops={"color": "white"}
)

st.pyplot(fig)

