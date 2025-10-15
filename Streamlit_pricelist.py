import pandas as pd
import streamlit as st

st.set_page_config(page_title="Turbo Lookup", page_icon="🔧", layout="centered")

# Styling with light/dark theme support
st.markdown("""
    <style>
    .stApp {
        font-family: 'Segoe UI', sans-serif;
    }
    .title-text {
        font-size: 2.5em;
        font-weight: 600;
        margin-bottom: 20px;
    }
    .result-box {
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    @media (prefers-color-scheme: light) {
        .stApp {
            background-color: #f2f6ff;
        }
        .title-text {
            color: #004085;
        }
        .result-box {
            background-color: #e9f2fb;
        }
    }
    @media (prefers-color-scheme: dark) {
        .stApp {
            background-color: #0e1117;
        }
        .title-text {
            color: #91cfff;
        }
        .result-box {
            background-color: #1e293b;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Load turbo data
file_path = "Prices (1).xlsx"
turbo_df = pd.read_excel(file_path, skiprows=1)
turbo_df.columns = ["PART #", "BRAND", "MANUFACTURER", "DESCRIPTION", "INTERCHANGE", "RRP without Actuator", "RRP with Actuator", "DEALER PRICE without actuator", "DEALER PRICE with actuator", "CORE", "INVENTORY"]
turbo_df["PART #"] = turbo_df["PART #"].astype(str)
turbo_df["INTERCHANGE"] = turbo_df["INTERCHANGE"].fillna("").astype(str)
turbo_df["DESCRIPTION"] = turbo_df["DESCRIPTION"].fillna("").astype(str)
turbo_df["BRAND"] = turbo_df["BRAND"].fillna("").astype(str)
turbo_df["MANUFACTURER"] = turbo_df["MANUFACTURER"].fillna("").astype(str)

# Load actuator data
actuator_df = pd.read_excel("Actuators_price list.xlsx", skiprows=1)
actuator_df.columns = ["PART #", "YEARS", "TURBO MODEL", "APPLICATION", "INTERCHANGE", "PRICE", "DEALER PRICE", "CORE"]
actuator_df = actuator_df.fillna("")
actuator_df["PART #"] = actuator_df["PART #"].astype(str)
actuator_df["INTERCHANGE"] = actuator_df["INTERCHANGE"].astype(str)

# Search by part number
def find_all_matches(part_number):
    part_number = part_number.strip()
    t_direct = turbo_df[turbo_df["PART #"] == part_number]
    t_inter = turbo_df[turbo_df["INTERCHANGE"].str.contains(part_number, na=False)]
    a_direct = actuator_df[actuator_df["PART #"] == part_number]
    a_inter = actuator_df[actuator_df["INTERCHANGE"].str.contains(part_number, na=False)]
    turbo_results = pd.concat([t_direct, t_inter]).drop_duplicates()
    actuator_results = pd.concat([a_direct, a_inter]).drop_duplicates()
    return turbo_results, actuator_results

# Keyword search
def keyword_search(query):
    query = query.lower().strip()
    if not query:
        return pd.DataFrame(), pd.DataFrame()
    keywords = query.split()
    t_mask = turbo_df.apply(lambda row: all(
        any(kw in str(row[col]).lower() for col in ["DESCRIPTION", "BRAND", "MANUFACTURER"])
        for kw in keywords), axis=1)
    a_mask = actuator_df.apply(lambda row: all(
        any(kw in str(row[col]).lower() for col in ["APPLICATION", "TURBO MODEL"])
        for kw in keywords), axis=1)
    return turbo_df[t_mask], actuator_df[a_mask]

# UI
st.markdown("<div class='title-text'>🔍 Turbo & Actuator Lookup</div>", unsafe_allow_html=True)

filter_choice = st.radio("Select category:", ["All", "Turbochargers only", "Actuators only"])
part_number = st.text_input("Enter a part number:")
keyword_input = st.text_input("Or search by keywords (e.g., 'Cummins X15', 'HE400VG'):")

results_turbo, results_actuator = pd.DataFrame(), pd.DataFrame()
if part_number:
    results_turbo, results_actuator = find_all_matches(part_number)
elif keyword_input:
    results_turbo, results_actuator = keyword_search(keyword_input)

if filter_choice == "Turbochargers only":
    results_actuator = pd.DataFrame()
elif filter_choice == "Actuators only":
    results_turbo = pd.DataFrame()

if not results_turbo.empty:
    st.subheader("🌀 Turbochargers")
    for _, result in results_turbo.iterrows():
        st.markdown("<div class='result-box'>", unsafe_allow_html=True)
        st.markdown(f"**Part #:** {result['PART #']}")
        st.markdown(f"**Brand:** {result['BRAND']}")
        st.markdown(f"**Manufacturer:** {result['MANUFACTURER']}")
        st.markdown(f"**Description:**\n{result['DESCRIPTION']}")
        st.markdown(f"**Interchange:** {result['INTERCHANGE']}")
        st.markdown(f"**RRP without Actuator:** {result['RRP without Actuator']}")
        st.markdown(f"**RRP with Actuator:** {result['RRP with Actuator']}")
        st.markdown(f"**Dealer Price without actuator:** {result['DEALER PRICE without actuator']}")
        st.markdown(f"**Dealer Price with actuator:** {result['DEALER PRICE with actuator']}")
        st.markdown(f"**Core Charge:** {result['CORE']}")
        st.markdown(f"**Inventory:** {result['INVENTORY']}")
        st.markdown("</div>", unsafe_allow_html=True)

if not results_actuator.empty:
    st.subheader("⚙️ Actuators")
    for _, row in results_actuator.iterrows():
        st.markdown("<div class='result-box'>", unsafe_allow_html=True)
        st.markdown(f"**Part #:** {row['PART #']}")
        st.markdown(f"**Years:** {row['YEARS']}")
        st.markdown(f"**Turbo Model:** {row['TURBO MODEL']}")
        st.markdown(f"**Application:** {row['APPLICATION']}")
        st.markdown(f"**Interchange:** {row['INTERCHANGE']}")
        st.markdown(f"**Price:** {row['PRICE']}")
        st.markdown(f"**Dealer Price:** {row['DEALER PRICE']}")
        st.markdown(f"**Core Charge:** {row['CORE']}")
        st.markdown("</div>", unsafe_allow_html=True)

if results_turbo.empty and results_actuator.empty and (part_number or keyword_input):
    st.error("No matching parts found.")

# Footer
st.markdown(
    "<hr style='margin-top:40px;'>"
    "<div style='text-align: center; opacity: 0.6;'>"
    "Made with ❤️ by Lola"
    "</div>",
    unsafe_allow_html=True
)

