import streamlit as st
import pandas as pd

def load_data(file):
    df = pd.read_excel(file)
    return df

def display_payslip(payslip_date, selected_employee, employee_data):
    st.markdown(f"#### Payslip")
    st.markdown(f"**Date:** {payslip_date.strftime('%Y-%m-%d')}")
    st.markdown(f"**Name:** {selected_employee}")
    st.markdown(f"**Salary:** {employee_data['SALARY'].iloc[0]} ({employee_data['DAYS'].iloc[0]} days)")
    st.markdown(f"**Overtime:** {employee_data['OT AMOUNT'].iloc[0]}")
    st.markdown(f"**Total:** Php {employee_data['GROSS PAY'].iloc[0]}")
    st.markdown(f"**Vale:** {employee_data['VALE'].iloc[0]}")
    st.markdown(f"**Advance:** {employee_data['Advance'].iloc[0]}")
    st.markdown(f"**Total Deduction:** Php {employee_data['T DED'].iloc[0]}")
    st.markdown(f"**Take Home Pay:** **Php {employee_data['THOME PAY'].iloc[0]}**")

def main():
    st.set_page_config(layout="wide", page_title="Payslip Generator", page_icon=":money_with_wings:")
    uploaded_file = st.sidebar.file_uploader("Upload Excel file", type=["xlsx"])
    payslip_date = st.sidebar.date_input("Select Payslip Date")

    if uploaded_file is not None:
        payslip_data = load_data(uploaded_file)

        if 'EMPLOYEE' not in payslip_data.columns:
            st.error("Error: The column 'EMPLOYEE' does not exist in the uploaded file.")
            return

        employee_list = payslip_data['EMPLOYEE'].unique()
        
        # Calculate the number of rows needed
        num_rows = (len(employee_list) + 4) // 5

        # Display payslips in a grid layout
        for i in range(num_rows):
            cols = st.columns(5)
            for j in range(5):
                index = i * 5 + j
                if index < len(employee_list):
                    selected_employee = employee_list[index]
                    filtered_data = payslip_data[(payslip_data['EMPLOYEE'] == selected_employee)]
                    if not filtered_data.empty:
                        with cols[j]:
                            display_payslip(payslip_date, selected_employee, filtered_data)
                    # Skip displaying warning for empty data
                    else:
                        continue

if __name__ == "__main__":
    main()
