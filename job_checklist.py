import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Job Application Tracker", layout="wide")
st.title("💼 Job Application Tracker")

# ---- Default Data ----
default_jobs = {
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

# ---- Session State Initialization ----
if "jobs" not in st.session_state:
    st.session_state.jobs = default_jobs.copy()
if "details" not in st.session_state:
    st.session_state.details = {
        title: {"status": "Not Applied", "notes": "", "date": datetime.today().strftime("%Y-%m-%d")}
        for title in st.session_state.jobs
    }

# ---- Sidebar: Reset ----
st.sidebar.header("🧰 Utilities")
if st.sidebar.button("🔁 Reset Progress"):
    st.session_state.jobs = default_jobs.copy()
    st.session_state.details = {
        title: {"status": "Not Applied", "notes": "", "date": datetime.today().strftime("%Y-%m-%d")}
        for title in st.session_state.jobs
    }
    st.sidebar.success("Progress reset. Refresh the page to update.")
    st.stop()

# ---- Add New Job ----
st.subheader("➕ Add a New Job")
with st.form("new_job_form", clear_on_submit=True):
    new_title = st.text_input("Job Title")
    new_link = st.text_input("Application Link (URL)")
    submitted = st.form_submit_button("Add Job")
    if submitted:
        if new_title and new_link:
            if new_title in st.session_state.jobs:
                st.warning("Job already exists.")
            else:
                st.session_state.jobs[new_title] = new_link
                st.session_state.details[new_title] = {
                    "status": "Not Applied",
                    "notes": "",
                    "date": datetime.today().strftime("%Y-%m-%d")
                }
                st.success(f"Added: {new_title}")
                st.experimental_rerun()
        else:
            st.warning("Please enter both a job title and a link.")

# ---- Job List ----
st.subheader("📋 Your Job Applications")

# Filter jobs by status
selected_filter = st.selectbox("Filter by Status", ["All"] + status_options)

status_colors = {
    "Not Applied": "gray",
    "Applied": "blue",
    "Interview": "orange",
    "Rejected": "red",
    "Offer": "green"
}
status_emojis = {
    "Not Applied": "📝",
    "Applied": "📬",
    "Interview": "🟡",
    "Rejected": "❌",
    "Offer": "✅"
}

for title, url in st.session_state.jobs.items():
    details = st.session_state.details[title]
    current_status = details["status"]

    # Apply filter
    if selected_filter != "All" and current_status != selected_filter:
        continue

    emoji = status_emojis.get(current_status, "")
    color = status_colors.get(current_status, "black")

    st.markdown(f"### <span style='color:{color}'>{emoji} [{title}]({url})</span>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 3, 2])

    with col1:
        status = st.selectbox(
            "Status", status_options, index=status_options.index(current_status), key=f"status_{title}"
        )
    with col2:
        notes = st.text_input("Notes", value=details["notes"], key=f"notes_{title}")
    with col3:
        date = st.date_input(
            "Date", value=datetime.strptime(details["date"], "%Y-%m-%d"), key=f"date_{title}"
        )

    # Save changes
    st.session_state.details[title] = {
        "status": status,
        "notes": notes,
        "date": date.strftime("%Y-%m-%d")
    }

    st.markdown("---")

st.success("✅ Your progress is saved while this session is open.")
