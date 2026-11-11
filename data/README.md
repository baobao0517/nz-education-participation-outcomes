# Data & Source Files

Original Education Counts source files are excluded from the repository, but can be downloaded from the official source pages:

- https://www.educationcounts.govt.nz/statistics/attendance
- https://www.educationcounts.govt.nz/statistics/school-leavers

To fully reproduce the data pipeline, put these **exact filenames** under `data/raw/`:

- `Regular-attendance-data-2022-2026-Term2.xlsx`
- `Machine-readable-school-leavers-2015-2025.zip`

Run:

```bash
python src/extract_attendance.py     # read official Excel with artifact_tool
python src/build_analysis.py         # streaming parse and validate 365k source CSV records
python src/render_site.py            # rebuild self-contained dashboard
python src/verify_sql.py             # independent SQLite checks
python -m unittest discover -s tests -v
```

`data/verified/` has the 90-row source-attendance aggregate extract and subsequent **derived public data tables** necessary for the dashboard and SQL. `outputs/dashboard_data.json` is the versioned snapshot rendered by the published website. No school-level or person-level individual data are distributed.

**Definitions:** Term 2 regular attendance >90% of enrolled time; school leaver NCEA Level 2 or above or equivalent. Geography: Regional Council, with `Area Outside` and `Not Applicable` treated explicitly for national reconciliation.
