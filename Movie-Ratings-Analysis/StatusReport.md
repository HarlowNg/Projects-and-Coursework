# IS477 Interim Status Report: Do Critics Matter? Analyzing the Relationship Between Critic Scores and Movie Popularity

## Overview

This report summarizes the team’s progress since the submission of the initial project plan. At this stage, all foundational data work—including acquisition, cleaning, and integration—has been successfully completed. The project now has a fully processed and merged dataset that is ready for exploratory and statistical analysis in the final milestone.

This milestone focused primarily on building a reliable and reproducible data pipeline. Significant effort was dedicated to resolving inconsistencies across datasets, standardizing key variables, and ensuring high data quality prior to analysis. The resulting dataset provides a strong basis for evaluating the relationship between critic scores and indicators of movie popularity.

The sections below provide detailed updates on each planned task, an updated timeline, key deviations from the original plan, and a discussion of challenges encountered during implementation.

---

## Task Updates

### ✅ Repository Setup
**Status: Complete**

The project repository has been fully initialized and organized to support reproducibility and collaboration. Standard best practices were followed, including the use of a `.gitignore` file to protect sensitive information such as API keys, and an `.env.example` file to document required environment variables.

Additionally, a `requirements.txt` file was created to ensure consistent dependency management across environments, along with a `LICENSE` (MIT). All datasets—both raw and processed—are stored in a structured `datasets/` directory, and notebooks are organized to clearly separate acquisition, cleaning, and analysis stages.

This setup ensures that the project can be easily reproduced and extended in future iterations.

Artifacts: `.gitignore`, `.env.example`, `requirements.txt`, `LICENSE`, `ProjectPlan.md`

---

### ✅ Data Acquisition — Rotten Tomatoes (`movie_info.csv`)
**Status: Complete**

The Rotten Tomatoes dataset was downloaded from [r/datasets](https://www.reddit.com/r/datasets/) and stored unmodified at `datasets/movie_info.csv`. The dataset contains 12,413 rows and 5 columns: `title`, `url`, `release_date`, `critic_score`, and `audience_score`. 

While the dataset provides broad coverage, initial inspection revealed several issues that required attention during the cleaning phase. Specifically, scores are stored as percentage strings (e.g., `"84%"`) and `release_date` uses two inconsistent formats, both of which were handled during the cleaning phase.

Artifact: `datasets/movie_info.csv`

#### Data Licensing and Terms of Use

The Rotten Tomatoes dataset used in this project was obtained from a publicly shared dataset on Reddit (r/datasets). However, it is important to note that the original data originates from Rotten Tomatoes, which is owned by Fandango Media. Rotten Tomatoes does not provide an official public API or open dataset for bulk download, and its website content is subject to its Terms of Use.

According to Rotten Tomatoes’ terms, automated data extraction (e.g., web scraping) and redistribution of their content may be restricted without explicit permission. As a result, the dataset used in this project should be considered an unofficial, third-party compilation rather than an authoritative or licensed data source.

To remain compliant with ethical data use standards, this project follows the following principles:

- The dataset is used strictly for educational and non-commercial purposes
- No attempt is made to redistribute or commercialize the data
- The dataset is treated as a secondary source, and its limitations are acknowledged
- Proper attribution is provided to Rotten Tomatoes as the original data provider
  
This limitation will be documented in the final report, and results derived from this dataset will be interpreted with the understanding that the data may not fully reflect the official or complete Rotten Tomatoes database.

---

### ✅ Data Acquisition — TMDB API (`tmdb_movies.csv`)
**Status: Complete**

TMDB movie metadata was collected using `tmdb_data_script.ipynb`, which queries the TMDB REST API `/search/movie` endpoint using titles from the RT dataset. The output was saved to `datasets/tmdb_movies.csv` with columns: `id`, `title`, `release_date`, `vote_average`, `vote_count`, `popularity`, and `overview`.

A total of **700 records** were retrieved, covering movies from 1970-1973, with only four titles failing to return a match, **resulting in a match rate exceeding 99%** for attempted queries. API credentials were securely managed using environment variables via `python-dotenv`, ensuring that sensitive information was not exposed in the repository.

Artifacts: `datasets/tmdb_movies.csv`, `tmdb_data_script.ipynb`

---

### ✅ Data Cleaning
**Status: Complete**

Both datasets have been cleaned in `analysis.ipynb`. The specific steps and outcomes for each dataset are documented below.

**Rotten Tomatoes (`movie_info.csv`):**
- Stripped `%` from `critic_score` and `audience_score` and cast both to numeric (`float64`)
- Extracted `release_year` from two inconsistent date formats using regex (`"Released Dec 16, 1970"` and bare `"1970"`)
- Normalized `title` into a `title_clean` column (lowercase, punctuation removed, whitespace collapsed)
- Dropped 3,114 rows with missing `critic_score` or unparseable `release_year`
- Deduplicated by keeping the highest `critic_score` entry per `title_clean` + `release_year`, removing 1,194 duplicate rows
- **Final RT clean shape: 8,105 rows × 7 columns**

**TMDB (`tmdb_movies.csv`):**
- Parsed `release_year` from `YYYY-MM-DD` format using `pd.to_datetime().dt.year`
- Normalized `title` into `title_clean` using the same function as above
- Dropped 2 rows with missing `release_date`
- Deduplicated on `id`, removing 101 duplicate TMDB records caused by repeated title queries in the fetch script
- **Final TMDB clean shape: 597 rows × 9 columns**

Artifact: `analysis.ipynb`, `datasets/rt_clean.csv`, `datasets/tmdb_clean.csv`

---

### ✅ Data Integration
**Status: Complete**

The two cleaned datasets were merged in `analysis.ipynb` using `pandas.merge()` with an inner join on `title_clean` and `release_year`. Original columns from both sources are retained in the merged output for provenance.

- **Merged shape: 255 rows × 12 columns**
- **Match rate vs TMDB clean: 42.7%** (255 of 597 unique TMDB records matched an RT entry)
- Only 3 rows have a missing `audience_score`; all other columns are fully populated
- Key columns in the merged dataset: `title`, `release_year`, `critic_score`, `audience_score`, `popularity`, `vote_count`, `vote_average`, `overview`

**Descriptive statistics of key analysis columns:**

| Statistic | critic_score | popularity | vote_count | vote_average |
|---|---|---|---|---|
| count | 255 | 255 | 255 | 255 |
| mean | 67.77 | 1.84 | 589.43 | 6.40 |
| std | 23.69 | 3.42 | 1685.09 | 0.74 |
| min | 0.00 | 0.16 | 3.00 | 4.11 |
| max | 100.00 | 41.09 | 22512.00 | 8.69 |

Artifact: `analysis.ipynb`, `datasets/merged_movies.csv`

---

### ⏳ Data Quality Assessment
**Status: Pending**

A formal data quality assessment will be conducted in the next phase. This will include evaluating completeness, identifying potential outliers, and analyzing match rates in greater detail.
Particular attention will be given to the distribution of popularity metrics and the potential influence of extreme values.

---

### ⏳ Workflow Documentation
**Status: Pending**

Comprehensive documentation of the data pipeline will be developed following the completion of the analysis. This will include step-by-step descriptions of data acquisition, cleaning, and integration processes to ensure reproducibility.

---

### ⏳ Exploratory Analysis
**Status: Pending**

This next phase will focus on analyzing the relationship between critic scores and popularity metrics. Planned analyses include correlation calculations, distribution visualizations, and potential segmentation by vote count or rating levels.

---

### ⏳ Metadata & Data Dictionary
**Status: Pending**

A detailed data dictionary will be created to document all variables, including definitions, data types, and sources. This will improve interpretability and transparency for future users of the dataset.

---

### ⏳ Final Report
**Status: Pending**

The final report will synthesize findings from the analysis phase, present conclusions, and discuss limitations and potential extensions of the project.

---

## Updated Timeline

All technical milestones—including repository setup, data acquisition, cleaning, and integration—have been completed on schedule. Remaining tasks primarily involve analysis, documentation, and reporting, which will be addressed collaboratively in the final phase.

| Task | Description | Start Date | End Date | Responsible | Status |
|---|---|---|---|---|---|
| Repository setup | Initialize GitHub repo, `.gitignore`, `.env.example`, folder structure | March 22 | April 1 | Flynn | ✅ Done |
| Data acquisition — RT | Load and inspect `movie_info.csv`, verify structure | March 22 | April 1 | Flynn | ✅ Done |
| Data acquisition — TMDB | Run `tmdb_data_script.ipynb` to collect 700 matched records via API |  March 24 | April 1 | Flynn | ✅ Done |
| Data cleaning | Parse dates, strip score formatting, handle missing values, normalize titles |  March 24 | April 1 | Flynn | ✅ Done |
| Data integration | Merge datasets on `title_clean` + `release_year` | March 30 | April 1 | Flynn | ✅ Done |
| Data quality assessment | Document completeness, duplicate rates, match rate, and outliers |  April 6 | April 30 | Harlow | ⏳ Pending |
| Workflow documentation | Document end-to-end pipeline steps for reproducibility |  April 8 | May 1 | Harlow | ⏳ Pending |
| Exploratory analysis | Correlation analysis, vote count distribution, decade-level trends | April 10 | May 2 | Both | ⏳ Pending |
| Metadata & data dictionary | Write column definitions and provenance notes |  May 2 | May 3 | Harlow | ⏳ Pending |
| Final report | Compile and write full project report in Markdown | May 3 | May 5 | Both | ⏳ Pending |

---

## Changes to the Project Plan

### TMDB Fetch Target Expanded: 500 → 700 Records

The original plan targeted 500 TMDB records. After running the script, we observed that the RT dataset contains many duplicate and closely related title entries (e.g., *The Aristocats*, *The French Connection* each appear multiple times). Because the script fetches one TMDB result per RT row rather than per unique title, the raw output included repeated TMDB records. We expanded the target to 700 to ensure a sufficient number of unique records survive deduplication. After cleaning, 597 unique TMDB records remained.

### Merged Dataset Scope is 1970–1973

Because the TMDB queries were based on the top portion of the Rotten Tomatoes dataset, which is sorted chronologically, the resulting data is concentrated from 1970 to 1973.

While this limitation does not prevent analysis of the core research question, it restricts the ability to generalize findings across different time periods. This constraint will be explicitly acknowledged in the final report.

### No Changes to Research Questions

Both core research questions remain unchanged from the project plan. Genre analysis remains excluded from the scope.

### No Feedback-Driven Changes

There are no changes to the Project Plan, but a more detailed timeline along with Rotten Tomatoes Terms of Use is updated in the progress report, following the comments from the Project Plan submission.

---

## Challenges and Issues

### Challenge 1: Duplicate Entries from the RT Dataset

**Issue:** The RT dataset contains multiple rows for the same movie (e.g., *The Aristocats* appears with and without a critic score; *The French Connection* appears several times). These duplicates were passed as separate TMDB search queries, resulting in repeated TMDB records.

**Resolution:** Resolved during cleaning. RT duplicates were resolved by keeping the entry with the highest `critic_score` per `title_clean` + `release_year`, removing 1,194 rows. TMDB duplicates were resolved by deduplicating on `id`, removing 101 rows.

### Challenge 2: Inconsistent `release_date` Formats in RT Dataset

**Issue:** The `release_date` column in `movie_info.csv` uses two different formats: `"Released Dec 16, 1970"` for most entries and a bare `"1970"` for others. Standard date parsing fails on both.

**Resolution:** Resolved using a regex pattern (`\b(19|20)\d{2}\b`) to extract the 4-digit year from either format. This worked reliably across all rows with a parseable date.

### Challenge 3: Score Columns Stored as Strings

**Issue:** `critic_score` and `audience_score` are stored as strings with a `%` suffix (e.g., `"84%"`), making them unusable for numerical analysis directly.

**Resolution:** Stripped the `%` character using `str.replace()` and cast to numeric using `pd.to_numeric(..., errors='coerce')`, which also safely handles any remaining non-numeric values by converting them to `NaN`.

### Challenge 4: Merged Dataset Limited to 1970–1973

**Issue:** Because the TMDB fetch script started from the top of the RT dataset (sorted chronologically), all fetched records cover only ~1970–1973 films. The resulting merged dataset of 255 rows covers a narrow time window, which limits decade-level trend analysis.

**Plan:** This will be documented as a known scope limitation in the final report. As a potential improvement, future iterations could re-run the TMDB fetch script targeting a broader or more recent slice of the RT dataset to improve temporal coverage.

---

## Individual Contribution Summaries

### Flynn Huynh - fhuynh2

I completed the technical work for this milestone. This included setting up the full repository structure, writing and running `tmdb_data_script.ipynb` to collect 700 TMDB records, and implementing the data cleaning and integration pipeline in `analysis.ipynb`. Cleaning steps covered score parsing, date extraction, title normalization, missing value handling, and deduplication for both datasets. The final merge produced `datasets/merged_movies.csv` with 255 records ready for analysis.

### Harlow Nguyen - harlown2

I completed the interim progress report and incorporated revisions based on feedback from the previous submission. In addition, I reviewed both datasets to ensure data quality and consistency after the cleaning phase. I also verified the integrity of the final merged dataset by testing the merge results, checking for missing values, and confirming that key variables were correctly aligned across sources. 
