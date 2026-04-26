import oracledb
import pandas as pd
import os

from dotenv import load_dotenv

load_dotenv()

user = os.getenv("DB_USER")
password = os.getenv("DB_PASS")
dsn = os.getenv("DB_DSN")
lib_dir = os.getenv("LIB_DIR")

# oracledb.init_oracle_client(lib_dir=lib_dir)
# Connect to Oracle
connection = oracledb.connect(
    user=user,
    password=password,
    dsn=dsn
)
cursor = connection.cursor()

# -----------------------------------
# CLEAR TABLES (child first!)
# -----------------------------------

cursor.execute("DELETE FROM Risk_Assessment")
cursor.execute("DELETE FROM Application_Review")
cursor.execute("DELETE FROM Loan_Application")
cursor.execute("DELETE FROM Applicant")
cursor.execute("DELETE FROM Loan_Officer")

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

# ===================================
# LOAD LOAN_OFFICER TABLE
# ===================================

officer_df = pd.read_csv("data/loan_officer.csv")

# Clean data properly
officer_df = officer_df.fillna("")

# Ensure correct types
officer_df["Officer_ID"] = officer_df["Officer_ID"].astype(str)
officer_df["Name"] = officer_df["Name"].astype(str)
officer_df["Branch"] = officer_df["Branch"].astype(str)

for _, row in officer_df.iterrows():
    cursor.execute("""
        INSERT INTO Loan_Officer
        (Officer_ID, Name, Branch)
        VALUES (:1, :2, :3)
    """, (
        row["Officer_ID"],
        row["Name"],
        row["Branch"]
    ))

connection.commit()

# ===================================
# LOAD APPLICATION_REVIEW TABLE
# ===================================

review_df = pd.read_csv("data/application_review.csv")

# Clean data properly
review_df = review_df.fillna("")

# Ensure correct types
review_df["ReviewDate"] = pd.to_datetime(review_df["ReviewDate"], format="%Y-%m-%d")

review_df["OfficerID"] = review_df["OfficerID"].astype(str)
review_df["LoanID"] = review_df["LoanID"].astype(str)
review_df["DecisionNotes"] = review_df["DecisionNotes"].astype(str)

for _, row in review_df.iterrows():
    cursor.execute("""
        INSERT INTO Application_Review
        (OfficerID, LoanID, ReviewDate, DecisionNotes)
        VALUES (:1, :2, :3, :4)
    """, (
        row["OfficerID"],
        row["LoanID"],
        row["ReviewDate"],
        row["DecisionNotes"]
    ))

connection.commit()

# ===================================
# LOAD RISK_ASSESSMENT TABLE
# ===================================

risk_df = pd.read_csv("data/risk_assessment.csv")

# Clean data properly
risk_df = risk_df.fillna("")

# Ensure correct types
risk_df["RiskScore"] = pd.to_numeric(risk_df["RiskScore"], errors="coerce")

risk_df["Assessment_Date"] = pd.to_datetime(risk_df["Assessment_Date"], format="%Y-%m-%d")

risk_df["LoanID"] = risk_df["LoanID"].astype(str)
risk_df["RiskLevel"] = risk_df["RiskLevel"].astype(str)

for _, row in risk_df.iterrows():
    cursor.execute("""
        INSERT INTO Risk_Assessment
        (LoanID, Assessment_Date, RiskScore, RiskLevel)
        VALUES (:1, :2, :3, :4)
    """, (
        row["LoanID"],
        row["Assessment_Date"],
        (row["RiskScore"]),
        row["RiskLevel"]
    ))

connection.commit()

# -----------------------------------
# DONE
# -----------------------------------

cursor.close()
connection.close()

print("Data loaded successfully.")
