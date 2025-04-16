import streamlit as st
import numpy as np
import pandas as pd

# Load dataset
df = pd.read_csv("merged.csv") #"C:\Users\Ayush Dubey\Desktop\testss\honeycomb_data.csv"



def get_best_rows(df, parameter, input_value, tolerance):
    st.write(f"### Received inputs - Parameter: {parameter}, Input Value: {input_value}, Tolerance: {tolerance}")
    #st.caption("All dimensions are in mm\nH: Height\tL: Length\tA: Amplitude of curved wall\tt: wall thickness")
    st.caption(
    "All dimensions are in mm  \n"
    "**H**: Height &emsp; **L**: Length &emsp; **A**: Amplitude of curved wall &emsp; **t**: wall thickness"
    )

    if parameter == "E11/Es":
        # Filter rows where e11 is within the tolerance range
        filtered_df = df[(df["E11/Es"] >= input_value - tolerance) & (df["E11/Es"] <= input_value + tolerance)]
        
        st.write("### Filtered DataFrame for E11/Es")
        st.dataframe(filtered_df)

        if filtered_df.empty:
            return None, None, None  # No matching rows

        # Get the 5 rows where nu12 is maximum and 5 rows where nu12 is minimum
        top_5_nu12 = filtered_df.nlargest(5, "NU12")
        bottom_5_nu12 = filtered_df.nsmallest(5, "NU12")

        # Best result: Row where nu12 is minimum
        best_row = bottom_5_nu12.iloc[0]

        return top_5_nu12, bottom_5_nu12, best_row

    elif parameter == "NU12":
        # Filter rows where nu12 is within the tolerance range
        filtered_df = df[(df["NU12"] >= input_value - tolerance) & (df["NU12"] <= input_value + tolerance)]
        
        st.write("### Filtered DataFrame for nu12")
        st.dataframe(filtered_df)

        if filtered_df.empty:
            return None, None, None  # No matching rows
        
        # Get the 5 rows where e11 is maximum and 5 rows where e11 is minimum
        top_5_e11 = filtered_df.nlargest(5, "E11/Es")
        bottom_5_e11 = filtered_df.nsmallest(5, "E11/Es")
        
        best_row = top_5_e11.iloc[0]  # Select the highest E11/Es row

        return top_5_e11, bottom_5_e11, best_row

# Streamlit UI
st.title("SRH Design Parameter")
#st.caption("All dimensions are in mm")

parameter = st.selectbox("Select Parameter", ["E11/Es", "NU12"])
input_value = st.number_input(f"Enter desired {parameter}", value=0.0, step=0.01)
tolerance = st.number_input("Enter tolerance", value=0.05, step=0.01)

if st.button("Find Result"):
    top_results, bottom_results, best_result = get_best_rows(df, parameter, input_value, tolerance)

    if top_results is None:
        st.error(f"No records found within the tolerance for {parameter}.")
    else:
        st.success("Results Found!")
        
        if parameter == "E11/Es":
            st.write("### Top 5 Rows with Maximum NU12")
            st.dataframe(top_results)
            st.write("### Top 5 Rows with Minimum NU12")
            st.dataframe(bottom_results)
            st.write("### Best Row (Minimum NU12)")
            st.dataframe(best_result.to_frame().T)

        else:  # parameter == "nu12"
            st.write("### Top 5 Rows with Maximum E11/Es")
            st.dataframe(top_results)
            st.write("### Top 5 Rows with Minimum E11/Es")
            st.dataframe(bottom_results)
            if best_result is not None:
                st.write("### Best Row (Maximum E11/Es)")
                st.dataframe(best_result.to_frame().T)
