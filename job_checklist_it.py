import streamlit as st 

st.title("Job Application Tracker")

# List of jobs with their application links
jobs = {
    "Trainee Data analyst": "https://www.adzuna.co.uk/jobs/details/4986013048?utm_campaign=google_jobs_apply&utm_source=google_jobs_apply&utm_medium=organic",
    "Data Analyst, Deloitte": "https://gb.bebee.com/job/67460146b4e585bf0c2da19583ecc6c7?utm_campaign=google_jobs_apply&utm_source=google_jobs_apply&utm_medium=organic",
    "Graduate Scheme - HO Digital": "https://www.civilservicejobs.service.gov.uk/csr/index.cgi?SID=b3duZXJ0eXBlPWZhaXImam9ibGlzdF92aWV3X3ZhYz0xOTU4MTIyJnVzZXJzZWFyY2hjb250ZXh0PTEzODQzNTMwMiZzZWFyY2hzb3J0PXNjb3JlJm93bmVyPTUwNzAwMDAmcGFnZWFjdGlvbj12aWV3dmFjYnlqb2JsaXN0JnNlYXJjaHBhZ2U9MSZwYWdlY2xhc3M9Sm9icw==",
    "IT Support Apprentice": "https://www.linkedin.com/jobs/view/4255199263",
    "Data Center Technician, Microsoft": "https://jobs.careers.microsoft.com/us/en/job/1829145/Data-Center-Technician?jobsource=linkedin/jobs/6952538?gh_src=00bdd2ae1",
    "IT Support Technician": "https://www.linkedin.com/jobs/view/4256882186",
    "Customer Support Technician, Hybrid": "https://alcumus.pinpointhq.com/postings/fe62f351-946a-4958-b9aa-431874242c78/applications/new?utm_medium=job_board&utm_source=linkedIn",
    "Service Desk Analyst": "https://www.linkedin.com/jobs/view/4255764277",
    "IT Service Desk Analyst": "https://www.linkedin.com/jobs/view/4252816741",
    "Service Desk Analyst": "https://www.linkedin.com/jobs/view/4251786334",
    "Service Desk Analyst, Hays": "https://www.linkedin.com/jobs/view/4255988653",
    "IT Service Desk Engineer": "https://www.linkedin.com/jobs/view/4242590705",
    "IT Support Officer, Welsh Rugby": "https://www.linkedin.com/jobs/view/4257017155",
    "AI Analyst": "https://www.linkedin.com/jobs/view/4250266675"   
}

st.write("Here are the jobs I'm planning to apply for. Click on the job title to view the application link.")

for job, link in jobs.items():
    # Display each job title as a clickable link with a checkbox to mark as applied
    checked = st.checkbox(f"[{job}]({link})")
    if checked:
        st.success(f"You have marked {job} as applied.")
    else:
        st.info(f"Click the checkbox to mark {job} as applied.")
