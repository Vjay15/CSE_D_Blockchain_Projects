import streamlit as st
import datetime
import re
import requests
import pandas as pd
import plotly.express as px

# --------------------------
# CONFIG
# --------------------------
NODE_URL = "http://localhost:5000"  # URL of your local node API

st.set_page_config(page_title="E-Aadhaar Blockchain", layout="wide")
st.title("🪪 E-Aadhaar Blockchain System")
st.write("A decentralized-like identity management demo using blockchain principles.")

menu = st.sidebar.radio("Navigation", ["Register Aadhaar", "View Blockchain", "Verify Chain"])

# --------------------------
# HELPER FUNCTIONS
# --------------------------
def fetch_chain():
    try:
        response = requests.get(f"{NODE_URL}/chain")
        if response.status_code == 200:
            return response.json()['chain']
    except:
        st.error("⚠️ Cannot reach the blockchain node.")
    return []

def add_record(name, aadhaar_no, gender, dob, address):
    payload = {
        "name": name,
        "aadhaar_no": aadhaar_no,
        "gender": gender,
        "dob": dob,
        "address": address
    }
    try:
        response = requests.post(f"{NODE_URL}/add_block", json=payload)
        if response.status_code == 201:
            return True, response.json()
        else:
            return False, response.text
    except Exception as e:
        return False, str(e)

# --------------------------
# Register New Aadhaar
# --------------------------
if menu == "Register Aadhaar":
    st.subheader("🧾 Register New Aadhaar")

    with st.form("aadhaar_form"):
        name = st.text_input("Full Name")
        aadhaar_no = st.text_input("Aadhaar Number (12 digits)")
        gender = st.selectbox("Gender", ["Select", "Male", "Female", "Other"])
        dob = st.date_input(
            "Date of Birth",
            min_value=datetime.date(1900, 1, 1),
            max_value=datetime.date.today()
        )
        address = st.text_area("Residential Address")
        submit = st.form_submit_button("Add Record")

    if submit:
        aadhaar_no_str = str(aadhaar_no).strip()

        # Validate all fields
        if not name or not aadhaar_no_str or gender == "Select" or not address:
            st.error("⚠️ Please fill all fields properly.")
        elif not re.fullmatch(r"\d{12}", aadhaar_no_str):
            st.error("⚠️ Aadhaar must be exactly 12 digits.")
        else:
            success, result = add_record(name, aadhaar_no_str, gender, str(dob), address)
            if success:
                st.success(f"✅ Aadhaar record for {name} added successfully!")
            else:
                st.error(f"❌ Could not add record: {result}")

# --------------------------
# View Blockchain Ledger
# --------------------------
elif menu == "View Blockchain":
    st.subheader("🔗 Blockchain Ledger")

    chain = fetch_chain()
    if chain:
        df = pd.DataFrame(chain)
        st.dataframe(df)

        # Remove genesis block for analytics
# Remove genesis block for analytics
    analytics_data = [b for b in chain if b["name"] != "Genesis"]
    if analytics_data:
        fig = px.pie(analytics_data, names="gender", title="Gender Distribution in Aadhaar Records")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No records found or node unavailable.")

# --------------------------
# Verify Blockchain
# --------------------------
elif menu == "Verify Chain":
    st.subheader("🧩 Verify Blockchain Integrity")
    chain = fetch_chain()
    if chain:
        # Simple validation: check hashes are unique
        hashes = [b["hash"] for b in chain]
        if len(hashes) == len(set(hashes)):
            st.success("✅ Blockchain is valid and secure.")
        else:
            st.error("⚠️ Blockchain has tampered data!")
    else:
        st.info("No blockchain data to verify.")
