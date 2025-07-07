import streamlit as st
import json
import os
from datetime import datetime

st.set_page_config(page_title="Job Application Tracker", layout="wide")
st.title("💼 Job Application Tracker")

# Local JSON file to save data
DATA_FILE = "job_data.json"

# Default hardcoded jobs (only used once)
default_jobs = {
    "Trainee Data Analyst": "https://www.adzuna.co.uk/jobs/details/4986013048?...",
    "Data Analyst, Deloitte": "https://gb.bebee.com/job/67460146b4e585bf0c2da19583ecc6c7?...",
    "Graduate Scheme - HO Digital": "https://www.civilservicejobs.service.gov.uk/...",
    "IT Support Apprentice": "https://www.linkedin.com/jobs/view/4255199263",
    "Data Center Technician, Microsoft": "https://jobs.careers.microsoft.com/us/en/job/1829145/...",
    "IT Support Technician": "https://www.linkedin.com/jobs/view/4256882186",
    "Customer Support Technician, Hybrid": "https://alcumus.pinpointhq.com/postings/fe62f351...",
    "Service Desk Analyst": "https://www.linkedin.com/jobs/view/4255764277",
    "IT Service Desk Analyst": "https://www.linkedin.com/jobs/view/4252816741",
    "Service Desk Analyst, Hays": "https://www.linkedin.com/jobs/view/4255988653",
    "IT Service Desk Engineer": "https://www.linkedin.com/jobs/view/4242590705",
    "IT Support Officer, Welsh Rugby": "https://www.linkedin.com/jobs/view/4257017155",
    "AI Analyst": "https://www.linkedin.com/jobs/view/4250266675"
}

# Status options
status_options = ["Not Applied", "Applied", "Interview", "Rejected", "Offer"]

# Load saved data or create a new file with defaults
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
else:
    # Initial structure
    data = {
        "jobs": default_jobs,
        "details": {}
    }
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# --- Sidebar Actions ---
st.sidebar.header("🧰 Utilities")

# Download button
st.sidebar.download_button(
    "📥 Download Backup",
    data=json.dumps(data, indent=2),
    file_name="job_data_backup.json",
    mime="application/json"
)

# Reset everything
if st.sidebar.button("🔁 Reset All Progress"):
    data = {
        "jobs": default_jobs,
        "details": {}
    }
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)
    st.sidebar.success("Progress has been reset. Refresh the page to see changes.")
    st.stop()

# --- Add New Job Section ---
st.subheader("➕ Add a New Job")
with st.form("new_job_form", clear_on_submit=True):
    new_title = st.text_input("Job Title")
    new_link = st.text_input("Application Link (URL)")
    submitted = st.form_submit_button("Add Job")
    if submitted:
        if new_title and new_link:
            if new_title in data["jobs"]:
                st.warning("Job already exists.")
            else:
                data["jobs"][new_title] = new_link
                data["details"][new_title] = {
                    "status": "Not Applied",
                    "notes": "",
                    "date": datetime.today().strftime("%Y-%m-%d")
                }
                with open(DATA_FILE, "w") as f:
                    json.dump(data, f, indent=2)
                st.success(f"Added: {new_title}")
                st.experimental_rerun()
        else:
            st.warning("Please enter both a job title and a link.")

# --- Main Job Checklist UI ---
st.subheader("📋 Your Job Applications")

for job, link in data["jobs"].items():
    st.markdown(f"### [{job}]({link})")

    col1, col2, col3 = st.columns([2, 3, 2])

    with col1:
        status = st.selectbox(
            "Status",
            status_options,
            index=status_options.index(
                data["details"].get(job, {}).get("status", "Not Applied")
            ),
            key=f"status_{job}"
        )

    with col2:
        notes = st.text_input(
            "Notes",
            value=data["details"].get(job, {}).get("notes", ""),
            key=f"notes_{job}"
        )

    with col3:
        date_str = data["details"].get(job, {}).get("date", datetime.today().strftime("%Y-%m-%d"))
        date = st.date_input(
            "Date",
            value=datetime.strptime(date_str, "%Y-%m-%d").date(),
            key=f"date_{job}"
        )

    # Save updates
    data["details"][job] = {
        "status": status,
        "notes": notes,
        "date": str(date)
    }

    st.markdown("---")

# Save to JSON file
with open(DATA_FILE, "w") as f:
    json.dump(data, f, indent=2)

st.success("✅ Progress saved locally.")
