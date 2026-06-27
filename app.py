"""Team weekly planning dashboard for Streamlit."""

from __future__ import annotations

import streamlit as st

from data import get_reports

st.set_page_config(
    page_title="Weekly Team Planner",
    page_icon="🗓️",
    layout="wide",
)

st.title("🗓️ Weekly Team Planner")
st.caption("A simple shared app for vibe-coding weekly reports, blockers, fixes, and next steps.")

st.markdown(
    """
    ### Project roles / 역할 분담
    - **Frontend + 앱 화면:** Streamlit pages and UI components
    - **데이터 저장:** Supabase table for weekly reports
    - **코드 협업:** GitHub branches, pull requests, and reviews
    - **배포:** Streamlit Community Cloud or another Streamlit hosting environment
    """
)

reports = get_reports()

total_reports = len(reports)
unique_members = len({report.get("member_name", "") for report in reports if report.get("member_name")})
open_issues = sum(1 for report in reports if report.get("issues"))
planned_next_steps = sum(1 for report in reports if report.get("next_steps"))

metric_cols = st.columns(4)
metric_cols[0].metric("Reports", total_reports)
metric_cols[1].metric("Members", unique_members)
metric_cols[2].metric("Issue notes", open_issues)
metric_cols[3].metric("Next steps", planned_next_steps)

st.divider()

left, right = st.columns([1.1, 0.9], gap="large")

with left:
    st.subheader("Recent weekly updates")
    if reports:
        for report in reports[:5]:
            with st.container(border=True):
                st.markdown(f"**{report.get('week_label', 'No week')} · {report.get('member_name', 'Unknown')}**")
                st.write(report.get("did", "No update yet."))
                if report.get("next_steps"):
                    st.caption(f"Next: {report['next_steps']}")
    else:
        st.info("No reports yet. Open **Weekly Report** from the sidebar to add the first update.")

with right:
    st.subheader("How to use")
    st.write(
        """
        1. Each teammate opens **Weekly Report** and writes what they did.
        2. Add blockers/issues and how they were fixed.
        3. Write concrete next steps for next week.
        4. Review everything in **Archive** before the meeting.
        """
    )
    st.success("Tip: Keep reports short, specific, and action-oriented.")