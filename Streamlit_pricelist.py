import pandas as pd
import streamlit as st

# Load data
file_path = "Prices (1).xlsx"
df = pd.read_excel(file_path, skiprows=1)
df.columns = ["PART #", "BRAND", "MANUFACTURER", "DESCRIPTION", "INTERCHANGE", "RETAIL PRICE", "DEALER PRICE"]
df["PART #"] = df["PART #"].astype(str)
df["INTERCHANGE"] = df["INTERCHANGE"].fillna("").astype(str)

# Search function
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

# Streamlit UI
st.set_page_config(page_title="Part Lookup", page_icon="🔧")
st.title("🔍 Turbocharger Part Lookup")

part_number = st.text_input("Enter a part number:")

if part_number:
    result = find_part(part_number)
    if result is not None:
        st.success("Part found!")
        st.markdown(f"**Part #:** {result['PART #']}")
        st.markdown(f"**Brand:** {result['BRAND']}")
        st.markdown(f"**Manufacturer:** {result['MANUFACTURER']}")
        st.markdown(f"**Description:**\n{result['DESCRIPTION']}")
        st.markdown(f"**Interchange:** {result['INTERCHANGE']}")
        st.markdown(f"**Retail Price:** ${result['RETAIL PRICE']}")
        st.markdown(f"**Dealer Price:** ${result['DEALER PRICE']}")
    else:
        st.error("Part not found.")
