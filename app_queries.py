CURRENT_LOANS = """
select
    l.loan_id,
    l.loanamount, 
    l.loanterm, 
    l.applicationdate
from loan_application l
where (
    l.status = 'Approved' and
    current_date - l.applicationdate < l.loanterm    
)
"""

AVERAGE_RISK_SCORE = """
select
    a.lastname || ', ' || a.firstname as applicantname,
    avg(r.riskscore) as averagerisk
from applicant a
inner join loan_application l
on (a.applicant_id = l.applicantid)
inner join risk_assessment r
on (l.loan_id = r.loanid)
group by a.applicant_id, applicantname
"""

APPLICANT_HISTORY = """
select
    a.lastname || ', ' || a.firstname as applicantname,
    a.credithistory,
    a.employmentstatus,
    sum(l.status = 'Approved') as approvedcount,
    sum(l.status = 'Pending') as pendingcount,
    sum(l.status = 'Rejected') as rejectedcount,
    count(l.status) as totalcount
from applicant a
inner join loan_application l
on (a.applicant_id = l.applicantid)
group by 
    a.applicant_id, 
    applicantname, 
    a.credithistory, 
    a.employmentstatus
"""

MONTHLY_REVIEW_COUNT = """
select
    sum(extract(month from v.reviewdate) = 1) as jan,
    sum(extract(month from v.reviewdate) = 2) as feb,
    sum(extract(month from v.reviewdate) = 3) as mar,
    sum(extract(month from v.reviewdate) = 4) as apr,
    sum(extract(month from v.reviewdate) = 5) as may,
    sum(extract(month from v.reviewdate) = 6) as jun,
    sum(extract(month from v.reviewdate) = 7) as jul,
    sum(extract(month from v.reviewdate) = 8) as aug,
    sum(extract(month from v.reviewdate) = 9) as sep,
    sum(extract(month from v.reviewdate) = 10) as oct,
    sum(extract(month from v.reviewdate) = 11) as nov,
    sum(extract(month from v.reviewdate) = 12) as dec,
    count(v.reviewdate) as total
from application_review v
"""

BRANCH_TOTALS = """
select
    o.branch,
    count(v.reviewdate) as applicationsreviewed
from loan_officer o
left join application_review v --left join because 0 count is acceptable
on (o.officer_id = v.officerid)
group by o.branch
"""
