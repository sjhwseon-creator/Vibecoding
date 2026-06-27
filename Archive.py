"""Weekly report archive page."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from data import get_reports

st.set_page_config(page_title="Archive", page_icon="📚", layout="wide")

st.title("📚 Archive")
st.caption("팀 전체 기록을 보고 주차, 담당자, 역할별로 확인합니다.")

reports = get_reports()

if not reports:
    st.info("No saved reports yet.")
    st.stop()

df = pd.DataFrame(reports)

filters = st.columns(3)
with filters[0]:
    selected_week = st.selectbox("Week", ["All"] + sorted(df["week_label"].dropna().unique().tolist(), reverse=True))
with filters[1]:
    selected_member = st.selectbox("Member", ["All"] + sorted(df["member_name"].dropna().unique().tolist()))
with filters[2]:
    selected_role = st.selectbox("Role", ["All"] + sorted(df["role"].dropna().unique().tolist()))

filtered = df.copy()
if selected_week != "All":
    filtered = filtered[filtered["week_label"] == selected_week]
if selected_member != "All":
    filtered = filtered[filtered["member_name"] == selected_member]
if selected_role != "All":
    filtered = filtered[filtered["role"] == selected_role]

st.subheader(f"{len(filtered)} report(s)")
st.dataframe(
    filtered[["week_label", "member_name", "role", "did", "issues", "fixes", "next_steps"]],
    use_container_width=True,
    hide_index=True,
)

st.divider()

for _, report in filtered.iterrows():
    with st.expander(f"{report['week_label']} · {report['member_name']} · {report['role']}"):
        st.markdown("**Done**")
        st.write(report.get("did") or "-")
        st.markdown("**Issues**")
        st.write(report.get("issues") or "-")
        st.markdown("**Fixes**")
        st.write(report.get("fixes") or "-")
        st.markdown("**Next steps**")
        st.write(report.get("next_steps") or "-")