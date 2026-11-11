# Methodology & Metric Definitions

## 1. Analytical design

This is a **descriptive, cross-sectional and time-series regional analysis**, not a policy impact evaluation. All 16 New Zealand Regional Councils are compared. The central question concerns **persistent disadvantage in participation and attainment and the allocation of further investigative attention**, not assigning school or community blame.

**Stage 1 (Participation):** 2022–2026 Term 2 regular-attendance trends; 2026 as the current view.  
**Stage 2 (Outcomes):** 2019–2025 school-leaver NCEA L2+ attainment, and 2025 equity, age and ethnic subgroup diagnostics.  
**Stage 3 (Integrated):** 2025 Term 2 attendance compared with 2025 L2+ school-leaver attainment, for the same 16 Regional Councils, but **not the same students**.

## 2. Regular Attendance

**Definition:** % of eligible students attending **more than 90%** of Term 2, where attendance is measured in half-days (per official Education Counts). This is a strict *threshold measure*, not the overall fraction of school days attended.

`regular attendance (%) = 100 × regular-attending students / eligible students`

Only **Term 2** is used for year-on-year comparisons to control for differing term effects and to take advantage of the established official Term 2 series. Term 2 2026 is the most recent fully published term at preparation time; Term 3 2026 results were **provisional**, not mixed into this analysis. The dataset uses state and state-integrated attendance statistics as defined by the official source.

For any region `r` and year `t`:

- `gap_att_pp(r,t) = rate_att(r,t) − rate_att(NZ,t)` (same-year national comparison).
- `annual_change_pp(r,t) = rate_att(r,t) − rate_att(r,t−1)`.
- `avg_annual_improvement_pp_year(r) = [rate_att(r,2026) − rate_att(r,2022)] / 4`.
- `years_below_NZ_2022_2026(r) = count of years where gap_att_pp(r,t) < 0`.
- `average_5y_gap(r) = mean of annual gap_att_pp(r,t) over 2022–2026`.

All percentage-point (pp) calculations are arithmetic differences between percentages, **not percentage relative growth**. Published attendance percentages are rounded to one decimal; count-derived ratios are checked against them (0.07 pp tolerance). The national trend is a student-weighted national aggregate, **not the unweighted mean of 16 regional rates**. A higher starting level leaves less headroom for improvement.

**2026 regional matrix** plots latest Term 2 attendance level vs average annual pp improvement. Horizontal/vertical comparison lines use national 2026 attendance and national 2022–26 annual improvement. No quadrant is a formal performance grade.

**Target:** The national government's target is **80% regular attendance by 2030**. The target is shown as a reference only—not as the expectation for 2026 or a forecast.

## 3. School-leaver NCEA Level 2+ attainment

**Definition:** percentage of school leavers who have achieved NCEA Level 2 or above, or specified equivalent qualifications, by the reporting cutoff. Not a single exam score and not a share of the currently enrolled school population. School-leaver statistics also include valid equivalent qualification pathways (including IB / Cambridge under the source definition).

`attainment (%) = 100 × leavers with NCEA L2+ or equivalent / all school leavers in the matching reporting group`

The official machine-readable CSV includes one `All Leavers` ethnicity row per unique leaver group *as a category*, as well as separate total-response ethnic categories. For distinct school-leaver totals, the code filters `Student: Ethnic Group = 'All Leavers'` **before summing**. For ethnicity-specific rates it filters a **single** named ethnicity, never sums across ethnicities. The achieved category is `Qualification: Level 2 or Above = 'NCEA Level 2 or above'` and both qualification categories form the denominator.

- `gap_ncea_pp(r,t) = NCEA_L2plus(r,t) − NCEA_L2plus(NZ,t)`.
- `years_below_NZ_2019_2025(r) = count of seven years where same-year gap_ncea_pp < 0`.
- `average_7y_gap(r) = mean of same-year gaps over 2019–2025`.

Use **NCEA L2+** as the sole primary outcome KPI. NCEA Level 3+ and retention statistics are *context* for follow-up discussions only and are not mixed into the headline regional performance score.

## 4. National comparison: the crucial regional attribution issue

In 2025, the national official school-leaver figures reconcile to **70,786 leavers**, **55,062 achieving L2+** → **77.8%**. These include **6,045 leavers** recorded with Regional Council `Not Applicable`, of whom **2,560** achieved L2+ (42.35%). The 16 attributable regions contain **64,741 leavers**, **52,502 achieving L2+**, for a pooled 16-region rate of **81.1%**.

**Reporting rule:** the official nationwide **77.8%** is the primary benchmark on the 2025 integrated quadrant and regional ranking. Do not add a competing green regional-only benchmark to the main visual. The **81.1%** attributable-region pool is retained in the technical notes and used solely as the comparator for **within-group** analyses that also exclude region-unattributable records. This avoids silently mixing incompatible geographic populations.

A region only 0.3 pp above all-NZ (e.g. Bay of Plenty) is **not** labelled successful. Quads are heuristic and not statistical significance thresholds.

## 5. 2025 school EQI, ethnicity and leaving-age subgroups

- **School Equity Index (EQI):** three official groups **Fewer / Moderate / More** barriers plus `Unassigned`. They describe the **average socioeconomic barriers faced by learners at a school**, not personal characteristics or school quality. Group *composition shares* sum to 100% including Unassigned, but **within-group NCEA percentages do not**.
- **Ethnicity:** total response; each school leaver may appear in more than one named ethnic group. Within-group rates use each group's denominator. Do **not** sum ethnicity counts or compare across groups as if they were mutually exclusive. n<30 rates are withheld in the interactive explorer, and counts are provided for other subgroups.
- **Leaving age:** `Left before 17th birthday` vs `Stayed until age 17 or above`. These are mutually exclusive. Earlier leaving is strongly connected with having less time to earn qualifications; this alone does not isolate an independent effect.

**Within-group comparison:** `region_group_rate − pooled_16_council_same_group_rate`, with the pool formed from count numerators and denominators, not a simple average of percentages. These are unadjusted descriptive comparisons and can reflect subgroup composition, school selection, local programmes and other unmeasured influences.

## 6. 2025 integrated quadrant

- X-axis = `attendance(r,2025 Term 2) − attendance(NZ,2025 Term 2)` (national **58.4%**).
- Y-axis = `NCEA_L2plus(r,2025 leavers) − NCEA_L2plus(NZ,2025 leavers)` (national **77.8%**).
- Four visual regimes: both below, attendance below / NCEA above, attendance above / NCEA below, both above; a value exactly 0 is treated as *on the baseline*, not forced into a quadrant.
- Display **only official zero-reference lines**. Interpret any point close to an axis with caution, especially given the geographical attribution sensitivity of the NCEA benchmark.

Pairing 2025 and 2025 improves calendar comparability but **does not create a matched cohort**. The results are region-level ecological associations. No student-level linkage, causal model, policy efficacy estimate, or p-value from the 16 regional observations is reported.

## 7. Data constraints and responsible interpretation

1. **Different populations:** Attendance covers eligible students enrolled in Term 2. NCEA covers people *leaving school* that year.
2. **Different reference windows:** 2026 attendance is a current snapshot; 2025 NCEA is the latest published outcomes. Do not pair 2026 attendance as if outcomes from the same cohort were known.
3. **Changing measurement rules:** attendance codes and reporting were updated from Term 1 2025, with periodic retrospective revisions; NCEA qualification requirements also evolved. Do not attribute changes directly to particular events.
4. **Unadjusted regional comparisons:** regional rates are influenced by size, school mix, mobility, demographics and factors not controlled for.
5. **Small cells and school-level confidentiality:** display suppression for subgroup n<30; no individual student or school-level release in this project.
6. **Association ≠ causation:** low participation and attainment appearing together does not establish which factor explains the other.
7. **Policy learning requires evaluation:** past reported practices may motivate evaluation, but attribution to a strategy requires evidence of implementation, suitable comparison and outcome measurement.

**Source definitions:** [Regular Attendance](https://www.educationcounts.govt.nz/statistics/attendance) · [School leavers and NCEA L2+](https://www.educationcounts.govt.nz/statistics/school-leavers) · [School Equity Index](https://www.educationcounts.govt.nz/data-services/code-sets-and-classifications/the-equity-index)
