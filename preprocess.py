# preprocess.py
import pandas as pd
import os
import random
from datetime import datetime, timedelta

from faker import Faker
fake = Faker()

import kagglehub

# Download latest version
path = kagglehub.dataset_download("altruistdelhite04/loan-prediction-problem-dataset")
path = os.path.join(path, "test_Y3wMUE5_7gLdaTN.csv")
# Load dataset
df = pd.read_csv(path)

os.makedirs("data", exist_ok=True)

# Create output folder
os.makedirs("data", exist_ok=True)

# Applicant Table
applicant_df = df[['ApplicantIncome', 'Credit_History']].copy()
applicant_df['Applicant_ID'] = ['A' + str(i+1) for i in range(len(applicant_df))]
applicant_df['FirstName'] = [fake.first_name() for _ in range(len(applicant_df))]
applicant_df['LastName'] = [fake.last_name() for _ in range(len(applicant_df))]
applicant_df['EmploymentStatus'] = df['Self_Employed'].fillna("No")
applicant_df.rename(columns={'Credit_History': 'CreditHistory'}, inplace=True)
applicant_df[['Applicant_ID', 'FirstName', 'LastName', 'EmploymentStatus', 'CreditHistory']]\
    .to_csv("data/applicant.csv", index=False)

# Loan Application Table
loan_df = df[['LoanAmount', 'Loan_Amount_Term']].copy()
loan_df['Loan_ID'] = ['L' + str(i+1) for i in range(len(loan_df))]

statuses = ["Approved", "Rejected", "Pending"]
loan_df['Status'] = [random.choice(statuses) for _ in range(len(loan_df))]

loan_df['ApplicationDate'] = "2026-01-01"
loan_df['ApplicantID'] = applicant_df['Applicant_ID']
loan_df.rename(columns={'Loan_Amount_Term': 'LoanTerm', 'Loan_Status': 'Status'}, inplace=True)
loan_df[['Loan_ID', 'LoanAmount', 'LoanTerm', 'ApplicationDate', 'Status', 'ApplicantID']]\
    .to_csv("data/loan_application.csv", index=False)

# Loan Officer (synthetic data)
officers = pd.DataFrame({
    'Officer_ID': ['O1', 'O2', 'O3'],
    'Name': ['Alice Johnson', 'Brian Smith', 'Carlos Gomez'],
    'Branch': ['Orlando', 'Tampa', 'Miami']
})
officers.to_csv("data/loan_officer.csv", index=False)

# Application Review (synthetic)
reviews = pd.DataFrame({
    'OfficerID': ['O1', 'O2', 'O3'],
    'LoanID': loan_df['Loan_ID'][:3],
    'ReviewDate': ['2026-01-02', '2026-01-03', '2026-01-04'],
    'DecisionNotes': ['Approved', 'Pending Review', 'Rejected']
})
reviews.to_csv("data/application_review.csv", index=False)

# Risk Assessment (synthetic)
risk = pd.DataFrame({
    'LoanID': loan_df['Loan_ID'][:3],
    'Assessment_Date': ['2026-01-02', '2026-01-03', '2026-01-04'],
    'RiskScore': [650, 720, 580],
    'RiskLevel': ['Medium', 'Low', 'High']
})
risk.to_csv("data/risk_assessment.csv", index=False)

print("CSV files created successfully!")