# GitHub and GitHub Pages Publication

## Status

As of **11 November 2026** the complete project is **built, validated and ready to publish**, but the separate public GitHub repository **does not yet exist**. The currently connected GitHub operations can update accessible repositories but cannot create a new repository. No live Pages URL is asserted as working at this stage.

## One account action needed first

1. Open https://github.com/new while signed in as `baobao0517`.
2. Repository name: **`nz-education-participation-outcomes`**.
3. Visibility: **Public**.
4. Create an initial **README** (recommended; ensures a default `main` branch is available for subsequent automated updates).
5. Create repository.

At that point, the project is ready for the files in this archive to be added. Use the repository's authenticated git connection / Work browser to upload the project contents, preserving directory structure. **Do not upload the official raw XLSX/ZIP**: they are excluded from the provided release archive.

## Local Git route (if you prefer command line)

After creating the empty repository on GitHub **without** adding an initial README:

```bash
cd nz-education-participation-outcomes
git init -b main
git add .
git commit -m "Publish validated NZ Education Participation & Outcomes Insights V1"
git remote add origin https://github.com/baobao0517/nz-education-participation-outcomes.git
git push -u origin main
```

If you created a README through GitHub, clone it first and copy the entire prepared project into the cloned folder **before** committing, so the two histories are not divergent.

## Activate GitHub Pages

1. Open repository **Settings** → **Pages**.
2. Build and deployment: **Deploy from a branch**.
3. Branch: **main**; folder: **/docs** → **Save**.
4. Wait for the **pages build and deployment** GitHub Action to report success, and open:

   https://baobao0517.github.io/nz-education-participation-outcomes/

This URL is the **expected** address, **not a verified live deployment** until the preceding steps succeed.

## Post-publication checks

- Dashboard loads and shows 64.3% Term 2 2026 national attendance and 77.8% 2025 national NCEA L2+.
- Switching the persistence heatmap shows 2022–2026 Attendance / 2019–2025 NCEA.
- Selecting a region updates the interactive regional details.
- The EQI / Leaving age / Ethnicity selector works and n<30 values are withheld.
- 2025 integrated four-quadrant displays all 16 regions; click Gisborne and Tasman.
- Methodology / data validation / executive summary HTML pages open.
- Source ZIP and XLSX are **absent** from the public repository.
- Replace the provisional publication-status note and tick the three GitHub / Pages status boxes after successful verification.
