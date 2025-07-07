import streamlit as st
import json
import os
from datetime import datetime

st.set_page_config(page_title="Job Application Tracker", layout="wide")
st.title("💼 Job Application Tracker")

DATA_FILE = "job_data.json"

default_jobs = {
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

status_options = ["Not Applied", "Applied", "Interview", "Rejected", "Offer"]

status_icons = {
    "Not Applied": "⬜",
    "Applied": "✅",
    "Interview": "🟡",
    "Rejected": "❌",
    "Offer": "🎉"
}

# Load existing data or create new one
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
else:
    data = {
        "jobs": default_jobs,
        "details": {
            job: {"status": "Not Applied", "notes": "", "date": datetime.today().strftime("%Y-%m-%d")}
            for job in default_jobs
        }
    }
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# Sidebar utilities
st.sidebar.header("🧰 Utilities")
if st.sidebar.button("🔁 Reset Progress"):
    data = {
        "jobs": default_jobs,
        "details": {
            job: {"status": "Not Applied", "notes": "", "date": datetime.today().strftime("%Y-%m-%d")}
            for job in default_jobs
        }
    }
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)
    st.sidebar.success("Progress reset. Refresh the page.")
    st.experimental_rerun()

# Add new job form
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

# Main job list with status icons
st.subheader("📋 Your Job Applications")

for job, link in data["jobs"].items():
    current_status = data["details"].get(job, {}).get("status", "Not Applied")
    icon = status_icons.get(current_status, "⬜")

    st.markdown(f"### {icon} [{job}]({link})")

    col1, col2, col3 = st.columns([2, 3, 2])
    details = data["details"][job]

    with col1:
        status = st.selectbox(
            "Status", status_options, index=status_options.index(details["status"]), key=f"status_{job}"
        )
    with col2:
        notes = st.text_input("Notes", value=details["notes"], key=f"notes_{job}")
    with col3:
        date = st.date_input(
            "Date", value=datetime.strptime(details["date"], "%Y-%m-%d"), key=f"date_{job}"
        )

    # Save updates immediately
    data["details"][job] = {
        "status": status,
        "notes": notes,
        "date": date.strftime("%Y-%m-%d")
    }

    st.markdown("---")

# Save all changes to file
with open(DATA_FILE, "w") as f:
    json.dump(data, f, indent=2)

st.success("✅ Your progress is saved locally on your machine.")
