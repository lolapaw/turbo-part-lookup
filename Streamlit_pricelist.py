import pandas as pd
import streamlit as st
import streamlit_authenticator as stauth

# --- Authentication ---
names = ["Admin"]
usernames = ["admin"]
passwords = ["turbo123"]

hashed_passwords = stauth.Hasher(passwords).generate()
authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
                                     "part_lookup_app", "abcdef", cookie_expiry_days=30)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status:
    st.set_page_config(page_title="Turbo Lookup", page_icon="🔧", layout="centered")
    st.markdown("""
        <style>
        .stApp {
            background-color: #f2f6ff;
            font-family: 'Segoe UI', sans-serif;
        }
        .title-text {
            color: #004085;
            font-size: 2.5em;
            font-weight: 600;
        }
        .result-box {
            background-color: #e9f2fb;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.1);
        }
        </style>
    """, unsafe_allow_html=True)

    # Load Excel data
    file_path = "Prices (1).xlsx"
    df = pd.read_excel(file_path, skiprows=1)
    df.columns = ["PART #", "BRAND", "MANUFACTURER", "DESCRIPTION", "INTERCHANGE", "RETAIL PRICE", "DEALER PRICE"]
    df["PART #"] = df["PART #"].astype(str)
    df["INTERCHANGE"] = df["INTERCHANGE"].fillna("").astype(str)

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

    st.markdown("<div class='title-text'>🔍 Turbocharger Part Lookup</div>", unsafe_allow_html=True)
    st.write("")

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

elif authentication_status is False:
    st.error("Incorrect username or password.")
elif authentication_status is None:
    st.warning("Please enter your username and password.")
