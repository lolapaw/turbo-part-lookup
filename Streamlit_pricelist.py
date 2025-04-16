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

# Load Excel file
file_path = "Prices (1).xlsx"
df = pd.read_excel(file_path, skiprows=1)
df.columns = ["PART #", "BRAND", "MANUFACTURER", "DESCRIPTION", "INTERCHANGE", "RETAIL PRICE", "DEALER PRICE", "CORE", "INVENTORY"]
df["PART #"] = df["PART #"].astype(str)
df["INTERCHANGE"] = df["INTERCHANGE"].fillna("").astype(str)
df["DESCRIPTION"] = df["DESCRIPTION"].fillna("").astype(str)
df["BRAND"] = df["BRAND"].fillna("").astype(str)
df["MANUFACTURER"] = df["MANUFACTURER"].fillna("").astype(str)

# Search by part number or interchange
def find_all_matches(part_number):
    part_number = part_number.strip()
    direct_matches = df[df["PART #"] == part_number]
    interchange_matches = df[df["INTERCHANGE"].str.contains(part_number, na=False)]
    combined = pd.concat([direct_matches, interchange_matches]).drop_duplicates()
    return combined

# Search by keywords
def keyword_search(query):
    query = query.lower().strip()
    if not query:
        return pd.DataFrame()
    keywords = query.split()
    mask = df.apply(lambda row: all(
        any(kw in str(row[col]).lower() for col in ["DESCRIPTION", "BRAND", "MANUFACTURER"])
        for kw in keywords), axis=1)
    return df[mask]

# User Interface
st.markdown("<div class='title-text'>🔍 Turbocharger Part Lookup</div>", unsafe_allow_html=True)

part_number = st.text_input("Enter a part number:")
keyword_input = st.text_input("Or search by keywords (e.g., 'Cummins X15', 'Detroit S60'):")

results = pd.DataFrame()
if part_number:
    results = find_all_matches(part_number)
elif keyword_input:
    results = keyword_search(keyword_input)

if not results.empty:
    for _, result in results.iterrows():
        st.markdown("<div class='result-box'>", unsafe_allow_html=True)
        st.markdown(f"**Part #:** {result['PART #']}")
        st.markdown(f"**Brand:** {result['BRAND']}")
        st.markdown(f"**Manufacturer:** {result['MANUFACTURER']}")
        st.markdown(f"**Description:**\n{result['DESCRIPTION']}")
        st.markdown(f"**Interchange:** {result['INTERCHANGE']}")
        st.markdown(f"**Retail Price:** ${result['RETAIL PRICE']}")
        st.markdown(f"**Dealer Price:** ${result['DEALER PRICE']}")
        st.markdown(f"**Core Charge:** ${result['CORE']}")
        st.markdown(f"**Inventory:** {result['INVENTORY']}")
        st.markdown("</div>", unsafe_allow_html=True)
elif part_number or keyword_input:
    st.error("No matching parts found.")

# Footer
st.markdown(
    "<hr style='margin-top:40px;'>"
    "<div style='text-align: center; opacity: 0.6;'>"
    "Made with ❤️ by Lola"
    "</div>",
    unsafe_allow_html=True
)
