# Official Sources & Data Provenance

## Primary sources

1. **New Zealand Ministry of Education — Education Counts, Attendance.**  
   https://www.educationcounts.govt.nz/statistics/attendance  
   Dataset: **2022–2026 Attendance data** (regular attendance, `Regional Council` worksheet), filtered to **Term 2** and regular attendance >90%.  
   Relevant official definition: percentage of eligible students attending more than 90% of term time, in half-days; government objective: 80% by 2030. Term 2 2026 was a complete published release; Term 3 2026 remained provisional at review time.

2. **New Zealand Ministry of Education — Education Counts, School leavers' attainment and destinations.**  
   https://www.educationcounts.govt.nz/statistics/school-leavers  
   Dataset: **Machine-readable school leavers, 2015–2025** (ZIP CSV); also checked against the **NCEA Level 2 or above 2015–2025** Excel time series. Primary KPI: school leavers who achieved NCEA Level 2 or above or equivalent at the reported school-leaver cutoff. The source includes unique leaver total rows and total-response ethnicity rows.

3. **New Zealand Ministry of Education — School Equity Index background.**  
   https://www.educationcounts.govt.nz/data-services/code-sets-and-classifications/the-equity-index  
   https://www.educationcounts.govt.nz/data-services/guidelines/school-equity-index-bands-and-groups  
   Used only to interpret school EQI group classification, not as evidence that EQI causes outcome differences.

## Secondary policy context

4. **Education Counts attendance reporting and definition changes.** The Attendance source page notes updates to reporting from Term 1 2025, including new attendance codes. These create a comparability caveat for trends.

5. **Ministry of Education attendance initiatives and evaluations.** References to attendance action plans / Regional Response Fund in project discussions are treated as *hypotheses for evaluation*, not documented causes of regional NCEA trends. Policy context should be verified independently before making claims about effective practices.

## Data handling and licence caution

- Original source ZIP and XLSX files were supplied for this portfolio analysis; the public repository excludes those binaries and includes only **small derived public regional / group aggregates** with proper attribution.
- Data remain attributed to **Education Counts / Ministry of Education**; the project does not claim official endorsement. Readers should check current Ministry usage / licensing terms before republishing source files or more granular data.
- The public interactive dashboard uses an inline JSON snapshot of derived counts and percentages, not third-party data collection or remote API access.

**As-of date:** 11 November 2026. Source data can be revised; date and original filenames are included in `data/README.md` and `docs/DATA_VALIDATION.md`.
