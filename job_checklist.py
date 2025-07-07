import streamlit as st
import json
import os
from datetime import datetime, date

st.set_page_config(page_title="Job Application Tracker", layout="wide")
st.title("💼 Job Application Tracker")

DATA_FILE = "job_data.json"

default_jobs = {
    "IT Support Engineer, Bristol": "https://www.linkedin.com/jobs/collections/recommended/?currentJobId=4232518920&origin=JYMBII_IN_APP_NOTIFICATION&originToLandingJobPostings=4258824691%2C4258198985",
    "Computer Security Research Intern, HP": "https://www.linkedin.com/jobs/collections/recommended/?currentJobId=4105049801&origin=JYMBII_IN_APP_NOTIFICATION&originToLandingJobPostings=4258824691%2C4258198985",
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

# --- Load or initialize data ---
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            pass  # fallback to default
    return {
        "jobs": default_jobs.copy(),
        "details": {
            job: {
                "status": "Not Applied",
                "notes": "",
                "date": datetime.today().strftime("%Y-%m-%d")
            } for job in default_jobs
        }
    }

data = load_data()

# --- Sidebar ---
st.sidebar.header("🧰 Utilities")
if st.sidebar.button("🔁 Reset Progress"):
    data = {
        "jobs": default_jobs.copy(),
        "details": {
            job: {
                "status": "Not Applied",
                "notes": "",
                "date": datetime.today().strftime("%Y-%m-%d")
            } for job in default_jobs
        }
    }
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)
    st.sidebar.success("Progress reset. Refresh the page.")
    st.experimental_rerun()

# --- Add a new job ---
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

# --- Display job applications ---
st.subheader("📋 Your Job Applications")

for job, link in data["jobs"].items():
    details = data["details"].get(job, {
        "status": "Not Applied",
        "notes": "",
        "date": datetime.today().strftime("%Y-%m-%d")
    })

    # Parse date safely
    try:
        parsed_date = datetime.strptime(details["date"], "%Y-%m-%d").date()
    except ValueError:
        parsed_date = date.today()

    icon = status_icons.get(details["status"], "⬜")
    st.markdown(f"### {icon} [{job}]({link})")

    col1, col2, col3 = st.columns([2, 3, 2])

    with col1:
        status = st.selectbox(
            "Status",
            status_options,
            index=status_options.index(details["status"]),
            key=f"status_{job}"
        )

    with col2:
        notes = st.text_input("Notes", value=details["notes"], key=f"notes_{job}")

    with col3:
        new_date = st.date_input("Date", value=parsed_date, key=f"date_{job}")

    # Update changes
    data["details"][job] = {
        "status": status,
        "notes": notes,
        "date": new_date.strftime("%Y-%m-%d")
    }

    st.markdown("---")

# --- Save to file ---
with open(DATA_FILE, "w") as f:
    json.dump(data, f, indent=2)

st.success("✅ Progress saved locally.")
