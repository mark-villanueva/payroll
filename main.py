import streamlit as st
import pandas as pd


def load_data(file):
    file_extension = file.name.split(".")[-1]
    if file_extension == "csv":
        df = pd.read_excel(file)
    else:
        raise ValueError("Unsupported file format. Only Excel (xlsx) and CSV files are supported.")
    return df


def display_payslip(payslip_date, selected_employee, employee_data):

    if not employee_data.empty:
        # Extracting data
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

        # Create table with grid lines
        st.markdown('<table style="border-collapse: collapse; border: 1px solid black;">'
                    '<tr><td colspan="2"><b>Date</b>: {}</td></tr>'
                    '<tr><td colspan="2"><b>Name</b>: {}</td></tr>'
                    '<tr><td><b>Salary</b>:</td><td>{}</td></tr>'
                    '<tr><td><b>Days</b>:<td>{}</td></tr>'
                    '<tr><td><b>Overtime</b>:</td><td>{}</td></tr>'
                    '<tr><td><b>Total</b>:</td><td>Php {}</td></tr>'
                    '<tr><td><b>Vale</b>:</td><td>{}</td></tr>'
                    '<tr><td><b>Advance</b>:</td><td>{}</td></tr>'
                    '<tr><td><b>Total Deduction</b>:</td><td>Php {}</td></tr>'
                    '<tr style="font-size: larger;"><td colspan="2"><b>Take Home Pay</b>:   <b>Php {}</b></td></tr>'
                    '</table>'.format(payslip_date.strftime('%Y-%m-%d'), selected_employee, salary, days, overtime, gross_pay, vale, advance, total_deduction, take_home_pay),
                    unsafe_allow_html=True)
    else:
        st.markdown("*No data available for this employee*")



def main():
    st.set_page_config(layout="wide", page_title="Payslip Generator", page_icon=":money_with_wings:")
    uploaded_file = st.sidebar.file_uploader("Upload Excel file", type=["csv"])
    payslip_date = st.sidebar.date_input("Select Payslip Date")

    if uploaded_file is not None:
        payslip_data = load_data(uploaded_file)

        if 'EMPLOYEE' not in payslip_data.columns:
            st.error("Error: The column 'EMPLOYEE' does not exist in the uploaded file.")
            return

        employee_list = payslip_data['EMPLOYEE'].unique()
        
        # Calculate the number of rows needed
        num_rows = (len(employee_list) + 2) // 3

        # Calculate the number of payslips that can fit in one page
        num_payslips_per_page = 3 * 3  # 3 rows, 3 columns

        # Custom CSS for adjusting left margin for printing and spacing between tables
        st.markdown("""
        <style>
        @media print {
            @page {
                margin-left: 0.05cm; /* Adjust as needed */ 
            }
        }
        .column-spacing {
            padding: 30px 10px; /* Adjust as needed */ 
        }
        </style>
        """, unsafe_allow_html=True)

        # Display payslips in a grid layout
        for i in range(0, num_rows):
            st.markdown("<div style='page-break-before: always;'> </div>", unsafe_allow_html=True)  # Page break for printing
            row = st.columns(3)
            start_index = i * num_payslips_per_page
            end_index = min(start_index + num_payslips_per_page, len(employee_list))
            for j in range(start_index, end_index):
                selected_employee = employee_list[j]
                filtered_data = payslip_data[(payslip_data['EMPLOYEE'] == selected_employee)]
                if not filtered_data.empty:
                    with row[j % 3]:
                        st.markdown('<div class="column-spacing"></div>', unsafe_allow_html=True)  # Add spacing between tables
                        display_payslip(payslip_date, selected_employee, filtered_data)

if __name__ == "__main__":
    main()
