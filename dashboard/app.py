import os
import pandas as pd
import requests
import streamlit as st

st.set_page_config(page_title="Email Fraud Triage",layout="wide")
st.title("Email Fraud Detection • Human-review dashboard")
st.caption("Risk is a heuristic indicator, not a verified probability. No messages are sent.")
api = st.sidebar.text_input("API URL",os.getenv("FRAUD_API_URL","http://localhost:8000"))
key = st.sidebar.text_input("API key",os.getenv("FRAUD_API_KEY",""),type="password")
sender = st.text_input("Sender")
recipient = st.text_input("Recipient")
subject = st.text_input("Subject")
body = st.text_area("Email content",height=220)
context = st.text_input("Company context","Operations and customer support")
if st.button("Classify and summarize"):
    try:
        response = requests.post(api.rstrip("/")+"/triage",json={"sender":sender,"recipient":recipient,"subject":subject,
          "body":body,"company_context":context},headers={"X-API-Key":key} if key else {},timeout=20)
        response.raise_for_status()
        r = response.json()
        a,b,c=st.columns(3)
        a.metric("Category",r["label"]);b.metric("Risk index",f'{r["risk_score"]:.2f}');c.metric("Priority",r["priority"])
        st.write("Reasons:",", ".join(r["reasons"]) or "No indicator matched")
        st.write("Summary:");st.write(r["summary"])
        st.write("Reply needed:",r["reply_needed"]," • Human approval:",r["review_required"])
        if r["proposed_reply"]:st.text_area("Suggested reply draft (not sent)",r["proposed_reply"])
    except requests.RequestException as ex:
        st.error(f"API request failed: {ex}")
