import streamlit as st
import pandas as pd
import numpy as np

st.title("Honeycomb Data Analysis App")

# Cache the data loading for performance
@st.cache_data
def load_data():
    # Load the dataset
    df = pd.read_csv("honeycomb_data.csv")
    return df

# Load dataset
df = load_data()

# Let the user select which parameter they want to input
parameter = st.selectbox("Select the parameter to input", ["e11", "nu12"])

# Input value for the chosen parameter
input_value = st.number_input(f"Enter the value for {parameter}:", value=0.0, step=0.001, format="%.3f")

if st.button("Find Result"):
    tolerance = 0.005  # tolerance level

    if parameter == "e11":
        # Filter rows where e11 is within the tolerance of the input
        filtered = df[np.abs(df["e11"] - input_value) <= tolerance]
        if filtered.empty:
            st.error("No records found within the tolerance for e11.")
        else:
            # Find the row with the closest e11 value
            closest_index = (np.abs(filtered["e11"] - input_value)).idxmin()
            closest_e11 = filtered.loc[closest_index, "e11"]
            # Find the minimum nu12 value among the filtered rows
            min_nu12 = filtered["nu12"].min()
            st.success("Result Found!")
            st.write(f"**Closest e11 value in dataset:** {closest_e11}")
            st.write(f"**Minimum nu12 value (among records within tolerance):** {min_nu12}")

    else:  # parameter == "nu12"
        # Filter rows where nu12 is within the tolerance of the input
        filtered = df[np.abs(df["nu12"] - input_value) <= tolerance]
        if filtered.empty:
            st.error("No records found within the tolerance for nu12.")
        else:
            # Find the row with the closest nu12 value
            closest_index = (np.abs(filtered["nu12"] - input_value)).idxmin()
            closest_nu12 = filtered.loc[closest_index, "nu12"]
            # Find the maximum e11 value among the filtered rows
            max_e11 = filtered["e11"].max()
            st.success("Result Found!")
            st.write(f"**Closest nu12 value in dataset:** {closest_nu12}")
            st.write(f"**Maximum e11 value (among records within tolerance):** {max_e11}")

# Optionally display the raw data for debugging or exploration
if st.checkbox("Show raw dataset"):
    st.write(df)
