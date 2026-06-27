"""Weekly report creation page."""

from __future__ import annotations

from datetime import date

import streamlit as st

from data import save_report

st.set_page_config(page_title="Weekly Report", page_icon="✍️", layout="wide")

st.title("✍️ Weekly Report")
st.caption("이번 주에 한 일, 이슈, 해결 방법, 다음 단계를 기록합니다.")

with st.form("weekly_report_form", clear_on_submit=True):
    col_a, col_b = st.columns(2)
    with col_a:
        member_name = st.text_input("Name / 이름", placeholder="예: Alex")
        role = st.selectbox(
            "Role / 담당 역할",
            [
                "Frontend + Streamlit UI",
                "Supabase data",
                "GitHub collaboration",
                "Deployment",
                "Project coordination",
            ],
        )
    with col_b:
        week_start = st.date_input("Week starting / 주 시작일", value=date.today())
        week_label = st.text_input("Week label / 주차", value=f"{date.today().isocalendar().year}-W{date.today().isocalendar().week:02d}")

    did = st.text_area("What did you do this week? / 이번 주 한 일", height=140)
    issues = st.text_area("Issues or blockers / 이슈 또는 막힌 점", height=110)
    fixes = st.text_area("How did you fix it? / 해결 방법", height=110)
    next_steps = st.text_area("Next steps / 다음 단계", height=110)

    submitted = st.form_submit_button("Save report / 저장", type="primary")

if submitted:
    if not member_name.strip() or not did.strip():
        st.error("Please enter at least your name and what you did this week.")
    else:
        save_report(
            {
                "member_name": member_name.strip(),
                "role": role,
                "week_start": week_start.isoformat(),
                "week_label": week_label.strip(),
                "did": did.strip(),
                "issues": issues.strip(),
                "fixes": fixes.strip(),
                "next_steps": next_steps.strip(),
            }
        )
        st.success("Report saved. You can review it in the Archive page.")