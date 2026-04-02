import oracledb
import pandas as pd

oracledb.init_oracle_client(lib_dir="/Users/nmacceus1/Desktop/instantclient")
# Connect to Oracle
connection = oracledb.connect(
    user="NMACCEUS_SCHEMA_FQ9YF",
    password="4JLBF!UG8zATB9996MT0ONA764SVM7",
    dsn="db.freesql.com:1521/23ai_34ui2"
)
cursor = connection.cursor()

# -----------------------------------
# CLEAR TABLES (child first!)
# -----------------------------------

cursor.execute("DELETE FROM Loan_Application")
cursor.execute("DELETE FROM Applicant")
connection.commit()

# ===================================
# LOAD APPLICANT TABLE
# ===================================

applicant_df = pd.read_csv("data/applicant.csv")

# Clean data properly
applicant_df = applicant_df.fillna("")

# Ensure correct types
applicant_df["Applicant_ID"] = applicant_df["Applicant_ID"].astype(str)
applicant_df["FirstName"] = applicant_df["FirstName"].astype(str)
applicant_df["LastName"] = applicant_df["LastName"].astype(str)
applicant_df["EmploymentStatus"] = applicant_df["EmploymentStatus"].astype(str)
applicant_df["CreditHistory"] = applicant_df["CreditHistory"].astype(str)

for _, row in applicant_df.iterrows():
    cursor.execute("""
        INSERT INTO Applicant
        (Applicant_ID, FirstName, LastName, EmploymentStatus, CreditHistory)
        VALUES (:1, :2, :3, :4, :5)
    """, (
        row["Applicant_ID"],
        row["FirstName"],
        row["LastName"],
        row["EmploymentStatus"],
        row["CreditHistory"]
    ))

connection.commit()

# ===================================
# LOAD LOAN_APPLICATION TABLE
# ===================================

loan_df = pd.read_csv("data/loan_application.csv")

# Clean whitespace
loan_df = loan_df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

# Convert numeric columns safely
loan_df["LoanAmount"] = pd.to_numeric(loan_df["LoanAmount"], errors="coerce")
loan_df["LoanTerm"] = pd.to_numeric(loan_df["LoanTerm"], errors="coerce")
loan_df = loan_df.dropna(subset=["LoanAmount", "LoanTerm"])

# Convert date column
loan_df["ApplicationDate"] = pd.to_datetime(loan_df["ApplicationDate"], format="%Y-%m-%d")

# Ensure string columns are strings
loan_df["Loan_ID"] = loan_df["Loan_ID"].astype(str)
loan_df["Status"] = loan_df["Status"].astype(str)
loan_df["ApplicantID"] = loan_df["ApplicantID"].astype(str)

for _, row in loan_df.iterrows():
    cursor.execute("""
        INSERT INTO Loan_Application
        (Loan_ID, LoanAmount, LoanTerm, ApplicationDate, Status, ApplicantID)
        VALUES (:1, :2, :3, :4, :5, :6)
    """, (
        row["Loan_ID"],
        (row["LoanAmount"]),
        (row["LoanTerm"]),
        row["ApplicationDate"],
        row["Status"],
        row["ApplicantID"]
    ))

connection.commit()

# -----------------------------------
# DONE
# -----------------------------------

cursor.close()
connection.close()

print("Data loaded successfully.")