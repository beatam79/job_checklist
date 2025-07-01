import streamlit as st
import json
import os

st.title("Job Application Tracker")

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
}

# File to save the checked states
STATE_FILE = "job_checklist_state.json"

# Load saved checkbox states from file or start fresh
if os.path.exists(STATE_FILE):
    with open(STATE_FILE, "r") as f:
        saved_states = json.load(f)
else:
    saved_states = {}

st.write("Here are the jobs I'm planning to apply for. Click on the job title to view the application link.")

# Function to save the states
def save_states(states):
    with open(STATE_FILE, "w") as f:
        json.dump(states, f)

# Loop through jobs and create checkboxes with saved state
for job, link in jobs.items():
    # Use saved state or False if none
    checked = saved_states.get(job, False)

    # Display checkbox, on_change saves new state
    new_state = st.checkbox(f"[{job}]({link})", value=checked, key=job)

    # Update saved state and save if changed
    if new_state != checked:
        saved_states[job] = new_state
        save_states(saved_states)

    if new_state:
        st.success(f"You have marked {job} as applied.")
    else:
        st.info(f"Click the checkbox to mark {job} as applied.")
