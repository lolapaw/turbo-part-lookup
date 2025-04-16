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
df.columns = ["PART #", "BRAND", "MANUFACTURER", "DESCRIPTION", "INTERCHANGE", "RETAIL PRICE", "DEALER PRICE"]
df["PART #"] = df["PART #"].astype(str)
df["INTERCHANGE"] = df["INTERCHANGE"].fillna("").astype(str)

# Search by part number or interchange
def find_part(part_number):
    part_number = part_number.strip()
    match = df[df["PART #"] == part_number]
    if not match.empty:
        return match.iloc[0]
    for _, row in df.iterrows():
        interchange_list = [x.strip() for x in row["INTERCHANGE"].split(",")]
        if part_number in interchange_list:
            return row
    return None

# User Interface
st.markdown("<div class='title-text'>🔍 Turbocharger Part Lookup</div>", unsafe_allow_html=True)

part_number = st.text_input("Enter a part number:")

if part_number:
    result = find_part(part_number)
    if result is not None:
        st.markdown("<div class='result-box'>", unsafe_allow_html=True)
        st.markdown(f"**Part #:** {result['PART #']}")
        st.markdown(f"**Brand:** {result['BRAND']}")
        st.markdown(f"**Manufacturer:** {result['MANUFACTURER']}")
        st.markdown(f"**Description:**\n{result['DESCRIPTION']}")
        st.markdown(f"**Interchange:** {result['INTERCHANGE']}")
        st.markdown(f"**Retail Price:** ${result['RETAIL PRICE']}")
        st.markdown(f"**Dealer Price:** ${result['DEALER PRICE']}")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.error("Part not found.")

# Footer
st.markdown(
    "<hr style='margin-top:40px;'>"
    "<div style='text-align: center; opacity: 0.6;'>"
    "Made with ❤️ by Lola"
    "</div>",
    unsafe_allow_html=True
)
