import streamlit as st
import json
import os
from datetime import date

# File to store application data
DATA_FILE = "job_data.json"

# Initial job list
jobs = {
    "Data Analyst, Deloitte": "https://gb.bebee.com/job/67460146b4e585bf0c2da19583ecc6c7?utm_campaign=google_jobs_apply&utm_source=google_jobs_apply&utm_medium=organic",
    "Graduate Data & Tech Programme": "https://www.whitbreadcareers.com/job-details/78585-4492/digital_data__technology_graduate_programme__september_2025_start",
    "Junior Web Analyst": "https://www.linkedin.com/jobs/view/4253264966",
    "Graduate Scheme - HO Digital": "https://www.civilservicejobs.service.gov.uk/csr/index.cgi?SID=b3duZXJ0eXBlPWZhaXImam9ibGlzdF92aWV3X3ZhYz0xOTU4MTIyJnVzZXJzZWFyY2hjb250ZXh0PTEzODQzNTMwMiZzZWFyY2hzb3J0PXNjb3JlJm93bmVyPTUwNzAwMDAmcGFnZWFjdGlvbj12aWV3dmFjYnlqb2JsaXN0JnNlYXJjaHBhZ2U9MSZwYWdlY2xhc3M9Sm9icw==",
    "Junior IT Support Engineer": "https://www.linkedin.com/jobs/view/4256510734",
    "IT Support Apprentice": "https://www.linkedin.com/jobs/view/4255199263",
    "Data Center Technician, Microsoft": "https://jobs.careers.microsoft.com/us/en/job/1829145/Data-Center-Technician?jobsource=linkedin/jobs/6952538?gh_src=00bdd2ae1",
    "IT Support Technician": "https://www.linkedin.com/jobs/view/4256882186",
    "Customer Support Technician": "https://alcumus.pinpointhq.com/postings/fe62f351-946a-4958-b9aa-431874242c78/applications/new?utm_medium=job_board&utm_source=linkedIn",
    "Service Desk Analyst": "https://www.linkedin.com/jobs/view/4255764277",
    "IT Service Desk Analyst": "https://www.linkedin.com/jobs/view/4252816741",
    "Service Desk Analyst": "https://www.linkedin.com/jobs/view/4251786334",
    "Service Desk Analyst, Hays": "https://www.linkedin.com/jobs/view/4255988653",
    "IT Service Desk Engineer": "https://www.linkedin.com/jobs/view/4242590705",
    "IT Support Officer, Welsh Rugby": "https://www.linkedin.com/jobs/view/4257017155",
    "AI Analyst": "https://www.linkedin.com/jobs/view/4250266675"
    # Add the rest of your jobs here...
}

# Load or initialize data
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        job_data = json.load(f)
else:
    job_data = {job: {"applied": False, "notes": "", "date": ""} for job in jobs}
    with open(DATA_FILE, "w") as f:
        json.dump(job_data, f)

st.title("Job Application Tracker")

# Filter
filter_option = st.selectbox("Filter jobs by:", ["All", "Applied", "Not Applied"])

st.write("### Jobs")
for job, link in jobs.items():
    data = job_data.get(job, {"applied": False, "notes": "", "date": ""})

    # Filter logic
    if filter_option == "Applied" and not data["applied"]:
        continue
    if filter_option == "Not Applied" and data["applied"]:
        continue

    with st.expander(job):
        st.markdown(f"[🔗 View Job Posting]({link})", unsafe_allow_html=True)
        applied = st.checkbox("Mark as applied", key=job, value=data["applied"])
        notes = st.text_area("Notes", value=data["notes"], key=f"{job}-notes")
        app_date = st.date_input("Application date", key=f"{job}-date", value=date.fromisoformat(data["date"]) if data["date"] else date.today())

        # Save on interaction
        job_data[job] = {
            "applied": applied,
            "notes": notes,
            "date": app_date.isoformat()
        }

# Save updates
with open(DATA_FILE, "w") as f:
    json.dump(job_data, f)

