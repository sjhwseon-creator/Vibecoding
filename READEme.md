# Weekly Team Planner

A small Streamlit joint project for weekly vibe-coding meetings. Teammates can record what they did, issues they met, how they fixed them, and next steps.

## Roles

- **Frontend + 앱 화면:** Streamlit (`app.py`, `pages/`)
- **데이터 저장:** Supabase (`utils/data.py`)
- **코드 협업:** GitHub branches and pull requests
- **배포:** Streamlit Community Cloud or another Streamlit deployment environment

## Project structure

```text
app.py                     # 첫 화면 / 대시보드
pages/1_Weekly_Report.py   # 기록 작성 폼
pages/2_Archive.py         # 전체 기록 보기
utils/data.py              # 저장, 불러오기, 데이터 처리
requirements.txt           # 필요한 Python 라이브러리 목록
```

## Supabase setup

Create a `weekly_reports` table with these columns:

| column | type |
| --- | --- |
| created_at | timestamptz |
| member_name | text |
| role | text |
| week_start | date |
| week_label | text |
| did | text |
| issues | text |
| fixes | text |
| next_steps | text |

Add the credentials to `.streamlit/secrets.toml` locally or to Streamlit Community Cloud secrets:

```toml
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_ANON_KEY = "your-supabase-anon-key"
```

If the secrets are not set, the app uses `data/weekly_reports.csv` as a local fallback for demos.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```