import streamlit as st
import numpy as np
import pandas as pd

df = pd.read_csv("honeycomb_data.csv")

def get_best_row(df, parameter, input_value, tolerance):
    if parameter == "e11":
        # Filter rows where e11 is within the tolerance range
        filtered_df = df[(df["e11"] >= input_value - tolerance) & (df["e11"] <= input_value + tolerance)]
        
        if filtered_df.empty:
            return None  # No matching rows

        # Find the row with the minimum nu12
        best_row = filtered_df.loc[filtered_df["nu12"].idxmin()]
        return best_row

    elif parameter == "nu12":
        # Filter rows where nu12 is within the tolerance range
        filtered_df = df[(df["nu12"] >= input_value - tolerance) & (df["nu12"] <= input_value + tolerance)]
        
        if filtered_df.empty:
            return None  # No matching rows
        
        # Find the row with the maximum e11
        best_row = filtered_df.loc[filtered_df["e11"].idxmax()]
        return best_row

# Streamlit UI
st.title("SRH Design Parameter")

# Load your DataFrame (df) here
# Example: df = pd.read_csv("your_data.csv")

parameter = st.selectbox("Select Parameter", ["e11", "nu12"])
input_value = st.number_input(f"Enter desired {parameter}")
tolerance = st.number_input("Enter tolerance", min_value=0.0, value=0.05)

if st.button("Find Result"):
    best_row = get_best_row(df, parameter, input_value, tolerance)

    if best_row is None:
        st.error(f"No records found within the tolerance for {parameter}.")
    else:
        st.success("Result Found!")
        st.write("**Best matching row:**")
        st.dataframe(best_row.to_frame().T)  # Display entire row as a DataFrame
