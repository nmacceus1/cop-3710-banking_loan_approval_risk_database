
CREATE TABLE Applicant (
    Applicant_ID VARCHAR2(10) PRIMARY KEY,
    FirstName VARCHAR2(50),
    LastName VARCHAR2(50),
    EmploymentStatus VARCHAR2(50),
    CreditHistory VARCHAR2(20)
);

CREATE TABLE Loan_Application (
    Loan_ID VARCHAR2(10) PRIMARY KEY,
    LoanAmount NUMBER,
    LoanTerm NUMBER,
    ApplicationDate DATE,
    Status VARCHAR2(20),
    ApplicantID VARCHAR2(10),
    FOREIGN KEY (ApplicantID) REFERENCES Applicant(Applicant_ID)
);

CREATE TABLE Loan_Officer (
    Officer_ID VARCHAR2(10) PRIMARY KEY,
    Name VARCHAR2(50),
    Branch VARCHAR2(50)
);

CREATE TABLE Application_Review (
    OfficerID VARCHAR2(10),
    LoanID VARCHAR2(10),
    ReviewDate DATE,
    DecisionNotes VARCHAR2(200),
    PRIMARY KEY (OfficerID, LoanID),
    FOREIGN KEY (OfficerID) REFERENCES Loan_Officer(Officer_ID),
    FOREIGN KEY (LoanID) REFERENCES Loan_Application(Loan_ID)
);

CREATE TABLE Risk_Assessment (
    LoanID VARCHAR2(10),
    Assessment_Date DATE,
    RiskScore NUMBER,
    RiskLevel VARCHAR2(20),
    PRIMARY KEY (LoanID, Assessment_Date),
    FOREIGN KEY (LoanID) REFERENCES Loan_Application(Loan_ID)
);
