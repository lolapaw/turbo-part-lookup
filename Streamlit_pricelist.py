import pandas as pd
import streamlit as st
from pyairtable import Table

st.set_page_config(page_title="Turbo Lookup", page_icon="🔧", layout="centered")

# Airtable setup for Turbochargers
AIRTABLE_TOKEN = "patXLEv6CLjVl6xYx.ff31913713df2ff59b0587e5215745174ddb298cff0eff0ac164364f4a9f2404"
BASE_ID = "appPn5AJmm53x5RXc"
TURBO_TABLE = "Turbo inventory"
turbo_table = Table(AIRTABLE_TOKEN, BASE_ID, TURBO_TABLE)
turbo_records = turbo_table.all()
turbo_df = pd.DataFrame([rec["fields"] for rec in turbo_records]).fillna("")

# Load Actuator Data from Excel
actuator_df = pd.read_excel("Actuators_price list.xlsx", skiprows=0).fillna("")

# Normalize
for df in [turbo_df, actuator_df]:
    df["PART #"] = df["PART #"].astype(str)
    df["INTERCHANGE"] = df["INTERCHANGE"].astype(str)

# Search functions
def find_all_matches(part_number):
    part_number = part_number.strip()
    t1 = turbo_df[turbo_df["PART #"] == part_number]
    t2 = turbo_df[turbo_df["INTERCHANGE"].str.contains(part_number, na=False)]
    a1 = actuator_df[actuator_df["PART #"] == part_number]
    a2 = actuator_df[actuator_df["INTERCHANGE"].str.contains(part_number, na=False)]
    return pd.concat([t1, t2]).drop_duplicates(), pd.concat([a1, a2]).drop_duplicates()

def keyword_search(query):
    query = query.lower().strip()
    if not query:
        return pd.DataFrame(), pd.DataFrame()
    keywords = query.split()
    turbo_mask = turbo_df.apply(lambda row: all(any(kw in str(row[col]).lower() for col in ["DESCRIPTION", "BRAND", "MANUFACTURER"]) for kw in keywords), axis=1)
    act_mask = actuator_df.apply(lambda row: all(any(kw in str(row[col]).lower() for col in ["APPLICATION", "TURBO MODEL"]) for kw in keywords), axis=1)
    return turbo_df[turbo_mask], actuator_df[act_mask]

# UI
st.markdown("<div class='title-text'>🔍 Turbo & Actuator Lookup</div>", unsafe_allow_html=True)

part_number = st.text_input("Enter a part number:")
keyword_input = st.text_input("Or search by keywords (e.g., 'Cummins X15', 'HE400VG'):")

results_turbo, results_actuator = pd.DataFrame(), pd.DataFrame()
if part_number:
    results_turbo, results_actuator = find_all_matches(part_number)
elif keyword_input:
    results_turbo, results_actuator = keyword_search(keyword_input)

if not results_turbo.empty:
    st.subheader("🌀 Turbochargers")
    for _, result in results_turbo.iterrows():
        st.markdown("<div class='result-box'>", unsafe_allow_html=True)
        st.markdown(f"**Part #:** {result.get('PART #', '')}")
        st.markdown(f"**Brand:** {result.get('BRAND', '')}")
        st.markdown(f"**Manufacturer:** {result.get('MANUFACTURER', '')}")
        st.markdown(f"**Description:**\n{result.get('DESCRIPTION', '')}")
        st.markdown(f"**Interchange:** {result.get('INTERCHANGE', '')}")
        st.markdown(f"**RRP without Actuator:** {result.get('RRP without Actuator', '')}")
        st.markdown(f"**RRP with Actuator:** {result.get('RRP with Actuator', '')}")
        st.markdown(f"**Dealer Price:** {result.get('DEALER PRICE', '')}")
        st.markdown(f"**Core Charge:** {result.get('CORE', '')}")
        st.markdown(f"**Inventory:** {result.get('INVENTORY', '')}")
        st.markdown("</div>", unsafe_allow_html=True)

if not results_actuator.empty:
    st.subheader("⚙️ Actuators")
    for _, result in results_actuator.iterrows():
        st.markdown("<div class='result-box'>", unsafe_allow_html=True)
        st.markdown(f"**Part #:** {result.get('PART #', '')}")
        st.markdown(f"**Years:** {result.get('YEARS', '')}")
        st.markdown(f"**Turbo Model:** {result.get('TURBO MODEL', '')}")
        st.markdown(f"**Application:** {result.get('APPLICATION', '')}")
        st.markdown(f"**Interchange:** {result.get('INTERCHANGE', '')}")
        st.markdown(f"**Price:** {result.get('PRICE', '')}")
        st.markdown(f"**Dealer Price:** {result.get('DEALER PRICE', '')}")
        st.markdown(f"**Core Charge:** {result.get('CORE', '')}")
        st.markdown("</div>", unsafe_allow_html=True)

if results_turbo.empty and results_actuator.empty and (part_number or keyword_input):
    st.error("No matching parts found.")

# Inventory manager
st.markdown("<hr><h4>🛠 Update Inventory (Turbo only)</h4>", unsafe_allow_html=True)
unique_parts = turbo_df["PART #"].dropna().unique()
selected_part = st.selectbox("Select Part to Update: ", unique_parts)
new_qty = st.number_input("Enter new inventory quantity:", min_value=0, step=1)
if st.button("Update Inventory"):
    for rec in turbo_records:
        fields = rec["fields"]
        if str(fields.get("PART #", "")) == selected_part:
            record_id = rec["id"]
            turbo_table.update(record_id, {"INVENTORY": int(new_qty)})
            st.success(f"Inventory for part {selected_part} updated to {new_qty} in Airtable.")
            break

# Footer
st.markdown(
    "<hr style='margin-top:40px;'>"
    "<div style='text-align: center; opacity: 0.6;'>"
    "Made with ❤️ by Lola"
    "</div>",
    unsafe_allow_html=True
)
