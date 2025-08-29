import streamlit as st
import pandas as pd

# ==========================
# Load Data
# ==========================
@st.cache_data
def load_data():
    df = pd.read_excel("Cleaned_Vehicle_Deployment.xlsx", sheet_name="Sheet1")

    # Drop first row if it's extra header
    df = df.drop(0).reset_index(drop=True)

    # Clean odometer column
    df["Odometer (Closing SPR)"] = pd.to_numeric(df["Odometer (Closing SPR)"], errors="coerce")

    # Clean Year
    df["Year of Manufacture"] = pd.to_numeric(df["Year of Manufacture"], errors="coerce")

    return df

df = load_data()

# ==========================
# Streamlit UI
# ==========================
st.set_page_config(page_title="Vehicle Deployment Ernakulam Rural", layout="wide")
st.title("🚓 Vehicle Deployment Ernakulam Rural")

# Sidebar filters
st.sidebar.header("Filters")

# 🔍 Search by Registration Number
search_reg = st.sidebar.text_input("Search by Registration Number (e.g., KL 01 BS 4971)").strip().upper()

vehicle_type = st.sidebar.multiselect(
    "Select Vehicle Type", options=df["Vehicle Type"].dropna().unique()
)

status = st.sidebar.multiselect(
    "Select Status (Onroad/Offroad)", options=df["Onroad/Offroad"].dropna().unique()
)

allotted = st.sidebar.multiselect(
    "Select Department/Unit", options=df["Allotted To"].dropna().unique()
)

# Apply filters only when something is selected
filtered_df = df.copy()

filters_applied = False

if search_reg:
    filtered_df = filtered_df[filtered_df["Reg No"].str.upper().str.contains(search_reg, na=False)]
    filters_applied = True

if vehicle_type:
    filtered_df = filtered_df[filtered_df["Vehicle Type"].isin(vehicle_type)]
    filters_applied = True

if status:
    filtered_df = filtered_df[filtered_df["Onroad/Offroad"].isin(status)]
    filters_applied = True

if allotted:
    filtered_df = filtered_df[filtered_df["Allotted To"].isin(allotted)]
    filters_applied = True

# ==========================
# Show Data (only if filters applied)
# ==========================
st.subheader("Filtered Vehicle Records")

if filters_applied:
    if not filtered_df.empty:
        st.dataframe(filtered_df, use_container_width=True)

        # ==========================
        # Key Statistics
        # ==========================
        st.subheader("📊 Summary Statistics")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total Vehicles", len(filtered_df))

        with col2:
            st.metric("Onroad Vehicles", (filtered_df["Onroad/Offroad"] == "Onroad").sum())

        with col3:
            st.metric("Offroad Vehicles", (filtered_df["Onroad/Offroad"] == "Offroad").sum())

    else:
        st.warning("No matching records found. Try adjusting your filters or search term.")
else:
    st.info("Please apply a filter or enter a search term to view vehicle records.")
