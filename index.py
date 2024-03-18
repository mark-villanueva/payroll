import streamlit as st
import pandas as pd


def load_data(file):
    df = pd.read_excel(file)
    return df

def display_payslip(payslip_date, selected_employee, employee_data):
    st.markdown(f"#### Payslip")
    st.markdown(f"**Date:** {payslip_date.strftime('%Y-%m-%d')}")
    st.markdown(f"**Name:** {selected_employee}")
    if not employee_data.empty:
        salary = employee_data['SALARY'].iloc[0]
        days = employee_data['DAYS'].iloc[0]
        overtime = employee_data['OT AMOUNT'].iloc[0]
        gross_pay = employee_data['GROSS PAY'].iloc[0]
        vale = employee_data['VALE'].iloc[0]
        advance = employee_data['Advance'].iloc[0]
        total_deduction = employee_data['T DED'].iloc[0]
        take_home_pay = employee_data['THOME PAY'].iloc[0]

        # Check for NaN values and replace with empty string
        salary = salary if pd.notna(salary) else ""
        days = days if pd.notna(days) else ""
        overtime = overtime if pd.notna(overtime) else ""
        gross_pay = gross_pay if pd.notna(gross_pay) else ""
        vale = vale if pd.notna(vale) else ""
        advance = advance if pd.notna(advance) else ""
        total_deduction = total_deduction if pd.notna(total_deduction) else ""
        take_home_pay = take_home_pay if pd.notna(take_home_pay) else ""

        st.markdown(f"**Salary:** {salary} ({days} days)")
        st.markdown(f"**Overtime:** {overtime}")
        st.markdown(f"**Total:** Php {gross_pay}")
        st.markdown(f"**Vale:** {vale}")
        st.markdown(f"**Advance:** {advance}")
        st.markdown(f"**Total Deduction:** Php {total_deduction}")
        st.markdown(f"**Take Home Pay:** Php {take_home_pay}")
    else:
        st.markdown("*No data available for this employee*")


def main():
    st.set_page_config(layout="wide", page_title="Payslip Generator", page_icon=":money_with_wings:", )
    uploaded_file = st.sidebar.file_uploader("Upload Excel file", type=["xlsx"])
    payslip_date = st.sidebar.date_input("Select Payslip Date")

    if uploaded_file is not None:
        payslip_data = load_data(uploaded_file)

        if 'EMPLOYEE' not in payslip_data.columns:
            st.error("Error: The column 'EMPLOYEE' does not exist in the uploaded file.")
            return

        employee_list = payslip_data['EMPLOYEE'].unique()
        
        # Calculate the number of rows needed
        num_rows = (len(employee_list) + 3) // 4

        # Calculate the number of payslips that can fit in one page
        num_payslips_per_page = 3 * 4  # 3 rows, 4 columns

        # Custom CSS for adjusting right margin
        st.markdown("""
        <style>
        .streamlit-container {
            max-width: 100%;
        }
        </style>
        """, unsafe_allow_html=True)

        # Display payslips in a grid layout
        for i in range(0, num_rows, 3):
            st.markdown("<div style='page-break-before: always;'> </div>", unsafe_allow_html=True)  # Page break for printing
            row1 = st.columns(4)
            row2 = st.columns(4)
            row3 = st.columns(4)
            for j in range(num_payslips_per_page):
                index = i * 4 + j
                if index < len(employee_list):
                    selected_employee = employee_list[index]
                    filtered_data = payslip_data[(payslip_data['EMPLOYEE'] == selected_employee)]
                    if not filtered_data.empty:
                        if j < 4:
                            with row1[j]:
                                display_payslip(payslip_date, selected_employee, filtered_data)
                        elif j < 8:
                            with row2[j - 4]:
                                display_payslip(payslip_date, selected_employee, filtered_data)
                        else:
                            with row3[j - 8]:
                                display_payslip(payslip_date, selected_employee, filtered_data)

if __name__ == "__main__":
    main()
