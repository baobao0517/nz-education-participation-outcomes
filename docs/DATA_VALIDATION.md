# Data Validation & Limitations

**Validation run:** 11 November 2026  
**Status:** Validated aggregates and reproducible checks; no causal / individual-level inferences.

## 1. Input provenance

| Input | Official source | User-provided file / handling |
|---|---|---|
| Term 2 regular attendance | Education Counts, *2022–2026 Attendance data* | `Regular-attendance-data-2022-2026-Term2.xlsx`; extract `Regional Council` worksheet using the documented 2022–2026 Term 2 filter. |
| NCEA school-leaver outcomes | Education Counts, *Machine-readable: School leavers (2015–2025)* | `Machine-readable-school-leavers-2015-2025.zip` containing one UTF-8 CSV, source kept outside the published repository. |
| Time series supporting cross-check | Education Counts, *NCEA Level 2 or above (2015–2025)* | `Time-series-School-leavers-NCEA-Level-2-2025.xlsx`; 2025 national and regional aggregates agree with reconstructed CSV data. |

**Geographic unit:** `Regional Council`; no mixing with Ministry's `Education Region` dimension.

## 2. Attendance source checks

- **90** validated Term 2 records = **16 Regional Councils × 5 years (80)** plus **national `All` × 5** and **`Area Outside` × 5**.
- `year + region` keys are unique. No missing combinations for the 16 councils in 2022–2026.
- All `regular_students <= students` and nonnegative; published `% regular` agrees with `100 × regular_students / students` to within **0.07 pp** rounding tolerance.
- For every year, sum of **16 councils + Area Outside** equals the **national `All`** for both student denominators and regular-attendance numerators.
- National percentages 2022–2026: **39.6%, 47.0%, 53.4%, 58.4%, 64.3%**.
- Raw workbook contains other terms and other metrics; only **Term 2**, **Regional Council**, and the **regular attendance** measure are selected. Source year-specific revisions and 2025 reporting changes matter.

## 3. School-leaver machine-readable ZIP checks

- ZIP contains one UTF-8 CSV with **28 columns** and **365,292 aggregate data records** for 2015–2025; **35,889** of those rows are dated 2025. Rows represent combinations of source dimensions, **not individual people**.
- Required fields checked: `Year: Left School`, `Region: Regional Council`, `Student: Ethnic Group`, `Student: Age (Retention To 17)`, `School: Equity Index Group`, `Qualification: Level 2 or Above`, `Students (∑ Values)`.
- Source `Qualification: Level 2 or Above` contains the two expected mutually exclusive statuses: `NCEA Level 2 or above` and `Below NCEA Level 2`.
- For unique denominators use **`Student: Ethnic Group = All Leavers`**. Never sum all the ethnicity rows together: the source also contains overlapping named ethnicity categories.
- For each of the 16 regions in 2025, age buckets reconcile to total leavers, and EQI buckets (`Fewer`, `Moderate`, `More`, `Unassigned`) reconcile to total leavers. All regions have results across 2019–2025.

### 2025 reconciliation

| Coverage | School leavers | NCEA Level 2+ achieved | Attainment |
|---|---:|---:|---:|
| 16 attributable Regional Councils | **64,741** | **52,502** | **81.10%** (calculated) |
| `Regional Council = Not Applicable` | **6,045** | **2,560** | **42.35%** |
| **All NZ** | **70,786** | **55,062** | **77.79% → 77.8% published** |

The all-NZ total is **not equal** to the sum of 16 region totals unless `Not Applicable` is included. The national official benchmark **77.8%** is used in the public quadrant and ranking. The region-attributable **81.1%** is used only as a transparent, like-for-like 16-region pool for subgroup diagnostics; it is **not represented as the official national benchmark**.

## 4. Join validation

- `attendance_2025(Regional Council)` joined **one-to-one** with `ncea_2025(Regional Council)` for **16** councils. No duplicate or missing region keys.
- 2026 attendance remains a standalone current participation view and is **never joined** to a 2026 NCEA rate (not yet published).
- Historical annual gaps compare each region to its **corresponding-year** national rate, not the latest national rate.
- Classification around 0 pp is descriptive; regions at 0.0 pp (e.g. Nelson 2025 attendance at published precision) are labelled *at baseline* rather than assigned arbitrarily.

## 5. Limitations, sensitivity and responsible use

- **Cohort mismatch:** Term 2 enrolled-student attendance and annual school-leaver qualifications refer to different student groups.
- **Small cohorts:** Some region × ethnic / EQI cells are small; the public subgroup explorer withholds `n<30` rates. Larger n does not remove confounding or cross-year volatility.
- **Ethnicity is total-response:** learners can appear in multiple groups. Their rows are not mutually exclusive.
- **School EQI measures average barriers:** it cannot diagnose any individual learner's socioeconomic condition or a school's teaching effectiveness.
- **Measurement changes:** The 2025 attendance coding/reporting changes and NCEA programme rules can affect long-term comparability.
- **Geographic sensitivity:** the unusually low NCEA attainment of `Not Applicable` leavers shifts the all-NZ reference downward. Apparent slight positive outliers can reverse using the pooled 16-region reference. This sensitivity is documented rather than cluttering the main graphic.
- **Noncausal:** no intervention effect, driver ranking, matched-cohort correlation, or statistical significance claim is made.
- **Source maintenance:** Revalidate if the Ministry publishes revisions; the extracted CSV and JSON reflect the named uploads as at 11 November 2026.

## 6. Automated validation / outputs

- `python src/extract_attendance.py` — source XLSX field, missing-key, duplicate, rounded-rate and national-count reconciliation (requires `artifact_tool`).
- `python src/build_analysis.py` — source ZIP schema / categories, 365,292 source row checks, unique leaver counts, regional / group reconciliations, 2019–2025 outcome trends.
- `python src/render_site.py` — builds a self-contained interactive `docs/index.html` from `outputs/dashboard_data.json`.
- `python src/verify_sql.py` — verifies SQL and one-to-one region joins using independent SQLite queries.
- `python -m unittest discover -s tests -v` — regression tests over published data and generated site.

Data extracts and JSON are published under `data/verified` / `outputs`. Original official source binaries are **excluded**, with authoritative source URLs documented in [SOURCES.md](SOURCES.md).
