import streamlit as st
import json
import os
from datetime import datetime

st.set_page_config(page_title="Job Application Tracker", layout="wide")
st.title("💼 Job Application Tracker")

DATA_FILE = "job_data.json"

default_jobs = {
    "IT Support Engineer, Bristol": "https://www.linkedin.com/jobs/collections/recommended/?currentJobId=4232518920&origin=JYMBII_IN_APP_NOTIFICATION&originToLandingJobPostings=4258824691%2C4258198985",
    "Computer Security Research Intern, HP": "https://www.linkedin.com/jobs/collections/recommended/?currentJobId=4105049801&origin=JYMBII_IN_APP_NOTIFICATION&originToLandingJobPostings=4258824691%2C4258198985",
    "Data Center Technician, Microsoft": "https://jobs.careers.microsoft.com/us/en/job/1829145/",
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

# ----- Load or create data -----
try:
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
        if "jobs" not in data or "details" not in data:
            raise ValueError("Invalid structure")
    else:
        raise FileNotFoundError
except (json.JSONDecodeError, FileNotFoundError, ValueError):
    data = {
        "jobs": default_jobs.copy(),
        "details": {
            job: {
                "status": "Not Applied",
                "notes": "",
                "date": datetime.today().strftime("%Y-%m-%d")
            }
            for job in default_jobs
        }
    }
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# ----- Sidebar -----
st.sidebar.header("🧰 Utilities")
if st.sidebar.button("🔁 Reset Progress"):
    data["jobs"] = default_jobs.copy()
    data["details"] = {
        job: {
            "status": "Not Applied",
            "notes": "",
            "date": datetime.today().strftime("%Y-%m-%d")
        }
        for job in default_jobs
    }
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)
    st.sidebar.success("Progress reset. Refresh the page to see changes.")
    st.stop()

# ----- Add a New Job -----
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

# ----- Display Jobs -----
st.subheader("📋 Your Job Applications")

for job, link in data["jobs"].items():
    st.markdown(f"### [{job}]({link})")

    col1, col2, col3 = st.columns([2, 3, 2])

    status = st.selectbox(
        "Status",
        status_options,
        index=status_options.index(data["details"][job]["status"]),
        key=f"status_{job}"
    )

    notes = st.text_input(
        "Notes",
        value=data["details"][job]["notes"],
        key=f"notes_{job}"
    )

    date_str = data["details"][job]["date"]
    date = st.date_input(
        "Date",
        value=datetime.strptime(date_str, "%Y-%m-%d"),
        key=f"date_{job}"
    )

    # Save back into data
    data["details"][job] = {
        "status": status,
        "notes": notes,
        "date": str(date)
    }

    st.markdown("---")

# ----- Save All Progress -----
with open(DATA_FILE, "w") as f:
    json.dump(data, f, indent=2)

st.success("✅ Progress saved to your local file.")
