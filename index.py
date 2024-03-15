import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# Function to load data from Excel file
def load_data(file):
    df = pd.read_excel(file)
    return df

# Function to display data for selected employee
def display_employee_data(df, selected_employee):
    employee_data = df[df['EMPLOYEE'] == selected_employee]
    return employee_data

# Function to generate HTML for payslip
def generate_payslip_html(payslip_date, selected_employee, employee_data):
    payslip_html = f"""
    <html>
    <head>
        <title>Payslip</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
            }}
            .payslip-container {{
                max-width: 600px;
                margin: 0 auto;
            }}
            .payslip-header {{
                text-align: center;
                margin-bottom: 20px;
            }}
            .payslip-details {{
                margin-bottom: 20px;
            }}
            .payslip-item {{
                margin-bottom: 10px;
            }}
        </style>
    </head>
    <body>
        <div class="payslip-container">
            <div class="payslip-header">
                <h2>Payslip</h2>
                <p>Date: {payslip_date.strftime('%Y-%m-%d')}</p>
                <p>Name: {selected_employee}</p>
            </div>
            <div class="payslip-details">
                <div class="payslip-item">
                    <p><strong>Salary:</strong> {employee_data['SALARY'].iloc[0]} ({employee_data['DAYS'].iloc[0]} days)</p>
                    <p><strong>Overtime:</strong> {employee_data['OT AMOUNT'].iloc[0]}</p>
                    <p><strong>Total:</strong> Php {employee_data['GROSS PAY'].iloc[0]}</p>
                </div>
                <div class="payslip-item">
                    <p><strong>Vale:</strong> {employee_data['VALE'].iloc[0]}</p>
                    <p><strong>Advance:</strong> {employee_data['Advance'].iloc[0]}</p>
                    <p><strong>Total Deduction:</strong> Php {employee_data['T DED'].iloc[0]}</p>
                    <p><strong>Take Home Pay:</strong> Php {employee_data['THOME PAY'].iloc[0]}</p>
                </div>
            </div>
        </div>
        <script>
            function printPayslip() {{
                window.print();
            }}
        </script>
    </body>
    </html>
    """
    return payslip_html

def main():
    st.title("Payslip Generator")

    # File upload
    file = st.file_uploader("Upload Excel file", type=["xlsx"])

    if file is not None:
        # Load data from Excel file
        df = load_data(file)

        # Display uploaded data
        st.write("### Uploaded Data:")
        st.write(df)

        # Dropdown menu to select employee
        employees = df['EMPLOYEE'].unique().tolist()
        selected_employee = st.selectbox("Select an employee", employees)

        # Date input for payslip date
        payslip_date = st.date_input("Payslip Date", value=pd.Timestamp.today())

        if selected_employee:
            # Display data for selected employee
            st.write("### Payslip for Selected Employee:")
            employee_data = display_employee_data(df, selected_employee)

            # Display payslip
            st.markdown(f"**Date:** {payslip_date.strftime('%Y-%m-%d')}")
            st.markdown(f"**Name:** {selected_employee}")
            st.markdown("---")
            st.markdown(f"**Salary:** {employee_data['SALARY'].iloc[0]} ({employee_data['DAYS'].iloc[0]} days)")
            st.markdown(f"**Overtime:** {employee_data['OT AMOUNT'].iloc[0]}")
            st.markdown(f"**Total:** Php {employee_data['GROSS PAY'].iloc[0]}")
            st.markdown("---")
            st.markdown(f"**Vale:** {employee_data['VALE'].iloc[0]}")
            st.markdown(f"**Advance:** {employee_data['Advance'].iloc[0]}")
            st.markdown(f"**Total Deduction:** Php {employee_data['T DED'].iloc[0]}")
            st.markdown(f"**Take Home Pay:** Php {employee_data['THOME PAY'].iloc[0]}")

            # Print button
            if st.button('Print Payslip'):
                payslip_html = generate_payslip_html(payslip_date, selected_employee, employee_data)
                st.write(payslip_html, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
