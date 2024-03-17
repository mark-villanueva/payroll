import streamlit as st
import pandas as pd\

# Function to load data from Excel or CSV file
def load_data(file):
    if file.name.endswith('.xlsx'):
        df = pd.read_excel(file)
    elif file.name.endswith('.csv'):
        df = pd.read_csv(file)
    else:
        st.error("Unsupported file format. Please upload an Excel (.xlsx) or CSV (.csv) file.")
        return None
    return df

# Function to display data for selected employee
def display_employee_data(df, selected_employee):
    employee_data = df[df['EMPLOYEE'] == selected_employee]
    return employee_data

# Function to generate HTML for payslip
def generate_payslip_html(payslip_date, selected_employee, employee_data):
    # Fill NaN values with empty string
    employee_data = employee_data.fillna('')

    if employee_data.empty:
        return ""  # Return empty string if no data available for this employee

    payslip_html = f"""
    <html>
    <head>
        <title>Payslip</title>
        <style>
            @media print {{
                @page {{
                    size: 3in 4in;
                    margin: 2mm;
                }}
                body {{
                    color: black !important;
                }}
                .page-break {{
                    page-break-before: always;
                }}
            }}
            body {{
                font-family: Arial, sans-serif;
            }}
            .payslip-container {{
                max-width: 600px;
                margin: 0 auto ;
            }}
            .payslip-header {{
                text-align: left;
                margin-bottom: 20px;
            }}
            .payslip-details {{
                margin-bottom: 10px;
            }}
            .payslip-item {{
                margin-bottom: 10px;
            }}
            .pay {{
                font-size: 20px;
            }}
        </style>
    </head>
    <body>
        <div class="payslip-container">
            <div class="payslip-header">
                <h3>Payslip</h3>
                <p><strong>Date:</strong> {payslip_date.strftime('%Y-%m-%d')}</p>
                <p><strong>Name:</strong> {selected_employee}</p>
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
                    <p class="pay"><strong>Take Home Pay:</strong> <strong>Php {employee_data['THOME PAY'].iloc[0]}</strong></p>
                </div>
            </div>
        </div>
        <div class="page-break"></div>
    </body>
    </html>
    """
    return payslip_html

def main():
    st.sidebar.title("Payslip Generator")

    # File upload
    file = st.sidebar.file_uploader("Upload Excel file", type=["xlsx", "csv"])

    if file is not None:
        # Load data from Excel file
        df = load_data(file)

        # Display uploaded data
        st.sidebar.write("### Uploaded Data:")
        st.sidebar.write(df)

        employees = df['EMPLOYEE'].unique().tolist()

        # Date input for payslip date
        payslip_date = st.sidebar.date_input("Payslip Date", value=pd.Timestamp.today())

        if st.sidebar.button('Generate Payslips'):
            for employee in employees:
                employee_data = display_employee_data(df, employee)
                payslip_html = generate_payslip_html(payslip_date, employee, employee_data)
                st.markdown(payslip_html, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
