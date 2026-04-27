import oracledb
import os
import time
from enum import IntEnum

import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from contextlib import contextmanager

import app_queries

class ErrorCodes(IntEnum):
    INVALID_CREDENTIALS = 1017
    TIMEOUT = 3113
    LOCKED = 28000

load_dotenv()    

USER = os.getenv("DB_USER")
PASS = os.getenv("DB_PASS")
DSN = os.getenv("DB_DSN")
LIB_DIR = os.getenv("LIB_DIR")

#oracledb.init_oracle_client(lib_dir=LIB_DIR)

st.set_page_config(page_title="Banking Loan Approval & Risk User Interface")

@contextmanager
def get_connection():
    try:
        with oracledb.connect(user=USER, password=PASS, dsn=DSN) as conn:
            yield conn
    
    except oracledb.DatabaseError as e:
        match e.args[0].code:
            case ErrorCodes.INVALID_CREDENTIALS:
                print("Connection error: Invalid credentials (Check LIB_DIR in .env)")
            case ErrorCodes.TIMEOUT:
                print("Connection error: Connection timeout")
            case ErrorCodes.LOCKED:
                print("Connection error: Database account is locked")
            case _:
                print(f"Connection error: ORA-{e.args[0].code}")
        raise
       
        
def get_query(query):
    with get_connection() as conn:
        with st.spinner("Fetching data..."):
            cursor = conn.cursor() # type: ignore
            
            cursor.execute(query)
            data_columns = [col[0] for col in cursor.description] # type: ignore
            display_data = pd.DataFrame(columns=data_columns)
        
        display_buffer = st.empty()
        
        while True:
            data_buffer = cursor.fetchmany(50)
            if not data_buffer:
                break
            df_buffer = pd.DataFrame(data_buffer, columns=data_columns)
            display_data = pd.concat([display_data, df_buffer], ignore_index=True)
            display_buffer.dataframe(display_data, hide_index=True)
            time.sleep(0.25)
        

st.sidebar.header("User Features")
selection = st.sidebar.radio("Select an option:", [
    "Current Loans", 
    "Average Risk Score", 
    "Applicant History", 
    "Monthly Review Count",
    "Branch Totals"
])

st.title(selection)
match selection:
    case "Current Loans":
        get_query(app_queries.CURRENT_LOANS)
    case "Average Risk Score":
        get_query(app_queries.AVERAGE_RISK_SCORE)
    case "Applicant History":
        get_query(app_queries.APPLICANT_HISTORY)
    case "Monthly Review Count":
        get_query(app_queries.MONTHLY_REVIEW_COUNT)
    case "Branch Totals":
        get_query(app_queries.BRANCH_TOTALS)
