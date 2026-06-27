"""Data access helpers for weekly reports.

The app stores records in Supabase when credentials are configured in
`.streamlit/secrets.toml`. For local demos without Supabase, it falls back to a
CSV file so the team can still test the workflow before deployment.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd
import streamlit as st
from supabase import Client, create_client

REPORT_COLUMNS = [
    "created_at",
    "member_name",
    "role",
    "week_start",
    "week_label",
    "did",
    "issues",
    "fixes",
    "next_steps",
]

LOCAL_DATA_PATH = Path("data/weekly_reports.csv")
SUPABASE_TABLE = "weekly_reports"


def _get_supabase_client() -> Client | None:
    """Return a Supabase client when secrets are available."""
    url = st.secrets.get("SUPABASE_URL")
    key = st.secrets.get("SUPABASE_ANON_KEY")
    if not url or not key:
        return None
    return create_client(url, key)


def _normalize_report(report: dict[str, Any]) -> dict[str, Any]:
    normalized = {column: report.get(column, "") for column in REPORT_COLUMNS}
    normalized["created_at"] = normalized["created_at"] or datetime.now(timezone.utc).isoformat()
    return normalized


def save_report(report: dict[str, Any]) -> None:
    """Save one weekly report to Supabase or local CSV fallback."""
    normalized = _normalize_report(report)
    client = _get_supabase_client()

    if client:
        client.table(SUPABASE_TABLE).insert(normalized).execute()
        return

    LOCAL_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    existing = _read_local_reports()
    updated = pd.concat([existing, pd.DataFrame([normalized])], ignore_index=True)
    updated.to_csv(LOCAL_DATA_PATH, index=False)


def get_reports() -> list[dict[str, Any]]:
    """Load reports newest first from Supabase or local CSV fallback."""
    client = _get_supabase_client()

    if client:
        response = client.table(SUPABASE_TABLE).select("*").order("created_at", desc=True).execute()
        return response.data or []

    local_reports = _read_local_reports()
    if local_reports.empty:
        return []
    local_reports = local_reports.fillna("").sort_values("created_at", ascending=False)
    return local_reports.to_dict(orient="records")


def _read_local_reports() -> pd.DataFrame:
    if not LOCAL_DATA_PATH.exists():
        return pd.DataFrame(columns=REPORT_COLUMNS)
    return pd.read_csv(LOCAL_DATA_PATH)