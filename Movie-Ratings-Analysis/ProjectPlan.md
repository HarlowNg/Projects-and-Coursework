# IS477 Project Plan: Do Critics Matter? Analyzing the Relationship Between Critic Scores and Movie Popularity

## Overview

Film critics often influence how movies are marketed and perceived by the public, but it is not always clear whether critical acclaim can translate into a movie's success from the audience. Our project aims to investigate whether critic scores are a meaningful predictor of a movie's popularity, using two complementary datasets: a Rotten Tomatoes dataset containing critic scores sourced from r/datasets, and enriched movie metadata fetched from The Movie Database (TMDB) API. By integrating these two sources, we aim to analyze **the relationship between critic evaluations, audience ratings, and how the popularity meaure up.**

To accomplish this goal, we will analyze two datasets: a **Rotten Tomato dataset** containing critic scores, and a **metadata from The Movie Database API that includes popularity metrics and vote counts.**  Our approach follows a standard data engineering and analysis pipeline. First, we will acquire and clean both datasets. Then, we normalize and merge them on movie `title` and `release year`. After performing a thorough data quality assessment producing an integrated dataset, we will conduct exploratory data analysis to investigate correlations and patterns. The project is motivated by a practically relevant question — does critical acclaim translate to popularity? — which has implications for studios, streaming platforms, and audiences alike. All code, data, and documentation are managed through GitHub with a fully automated and reproducible workflow!

---

## Team

| Member | Role & Responsibilities |
|---|---|
| Flynn Huynh - fhuynh2 | Data acquisition (Python scripting + API), data integration (Pandas merge), Git repository management |
| Harlow Nguyen - harlown2 | Data quality assessment, workflow organization, documentation, and report writing |

> *Note:* Our individual contributions might **NOT BE FULLY** reflected in the Git commit history. We frequently working collaboratively on the same device.

---

## Research Questions

1. **Is there a statistically meaningful correlation between a movie's critic score and its TMDB popularity score?**
2. **Do critically acclaimed movies (high critic score) tend to have higher vote counts and popularity, or does popularity operate independently of critical reception?**

These questions are directly answerable through the integration of the two datasets: Rotten Tomatoes provides the critic scores, while TMDB provides popularity scores and vote counts metadata. By comparing critic evaluations with audience ratings, we aim to better understand whether professional reviews align with public interest. 

---

## Datasets

### Dataset 1: Rotten Tomatoes Movie Scores (`movie_info.csv`)

- **Source:** [r/datasets](https://www.reddit.com/r/datasets/) (an approved course data source)
- **Format:** CSV (flat tabular file)
- **Access method:** Direct file download on reddit
- **Size:** 12,413 rows × 5 columns
- **Columns:** `title`, `url`, `release_date`, `critic_score`, `audience_score`
- **Coverage:** Movies from approximately 1970 to present
- **Relevance:** Provides the primary independent variable for our analysis — `critic_score` — which we use to investigate its relationship with TMDB popularity.
- **License/Ethics:** Shared publicly on r/datasets, referencing publicly accessible Rotten Tomatoes pages. No personally identifiable information is present. Used strictly for non-commercial educational purposes.

### Dataset 2: TMDB Movie Metadata (via API)

- **Source:** [The Movie Database (TMDB)](https://www.themoviedb.org/) — REST API v3
- **Format:** JSON (fetched via API, stored as CSV after transformation)
- **Access method:** HTTP REST API using a registered API key (`/search/movie` endpoint)
- **Columns collected:** `id`, `title`, `release_date`, `vote_average`, `vote_count`, `popularity`, `overview`
- **Coverage:** 500 matched records sourced by querying titles from the Rotten Tomatoes dataset
- **Relevance:** Provides the key dependent variables — `popularity` and `vote_count` — which serve as proxies for a movie's public reach and audience engagement, complementing the critic scores from Dataset 1.
- **License/Ethics:** Collected in compliance with [TMDB Terms of Use](https://www.themoviedb.org/terms-of-use) for non-commercial, educational use with attribution. No personal data is involved.
 **The API key is stored securely in a `.env` file and is never committed to GitHub since we don't want Flynn's API key to be exposed**

### Integration Strategy

The datasets share common attributes such as `title` and `release_date`, which will serve as the primary integration keys. To prepare the data for merging, we will:

- Normalize movie titles by converting them to lowercase, remove whitespace and punctuation.
- Extract release year from full release date in both datasets
- Create a standardized `title_clean` column in both datasets

The cleaned title and release year will then be used as join keys when merging the datasets using `pandas.merge()`. Original columns will be retained to preserve provenance and allow traceability back to the source datasets.

---

## Data Lifecycle

Our project will follow the **USGS Science Data Lifecycle Model** from our lecture due to its simplicity:

- **Plan:** We together define the above research questions, identify datasets, outline roles, storage strategy, and ethical considerations.
- **Acquire:** Download the Rotten Tomatoes CSV from r/datasets; fetch TMDB metadata via REST API using a Python script (`tmdb_data_script.ipynb`).
- **Process:** We plan to clean both datasets (parse dates, strip score formatting, handle missing values, normalize titles); merge on shared identifiers.
- **Analyze:** We will perform correlation analysis between critic scores and TMDB popularity; examine vote count distributions; explore decade-level trends using Python.
- **Preserve:** We store raw data unmodified in the `datasets/` directory; maintain full Git history for provenance; document data lineage and transformations.
- **Publish/Share:** We plan to publish the completed project, report, and reproducible workflow as a GitHub release; include metadata and a data dictionary to support reuse.

---

## Storage and Organization

```
project/
├── datasets/
│   ├── movie_info.csv          # Raw RT dataset (original, unmodified)
│   └── tmdb_movies.csv         # TMDB data fetched via API
├── tmdb_data_script.ipynb      # API data collection and export
├── .env                        # API key (gitignored, never pushed)
├── .env.example                # API key placeholder (committed)
├── .gitignore
├── LICENSE
├── requirements.txt
└── ProjectPlan.md
```

Raw data files are stored unmodified in `datasets/` to support provenance and reproducibility. The TMDB script fetches, transforms, and saves data directly to this folder. The project uses flat CSV as the primary storage format for portability and ease of integration with Pandas.

---

## Ethical Data Handling

- **Rotten Tomatoes data:** Sourced from r/datasets (an approved course source) and used strictly for educational purposes. No live scraping is performed.
- **TMDB data:** Collected in compliance with TMDB's Terms of Use (non-commercial, educational use with attribution). Attribution will be included in the final report.
- **API key security:** Stored in a local `.env` file, excluded from version control via `.gitignore`. A `.env.example` placeholder is committed in its place.
- **No personal data:** Neither dataset contains personally identifiable information. No consent issues apply.
- **Reproducibility:** A `requirements.txt` and `.env.example` allow others to reproduce the full workflow without exposing any credentials.

---

## Timeline

| Task | Description | Responsible | Status |
|---|---|---|---|
| Repository setup | Initialize GitHub repo, `.gitignore`, `.env.example`, folder structure | Flynn | ✅ Done |
| Data acquisition — RT | Load and inspect `movie_info.csv`, verify structure and completeness | Flynn | ✅ Done |
| Data acquisition — TMDB | Finalize and run `tmdb_data_script.ipynb` to collect 500 records | Flynn | ✅ Done |
| Data cleaning | Parse dates, strip score formatting, handle missing values, normalize titles in both datasets | Flynn | In Progress |
| Data integration | Merge datasets on `title_clean` + release year | Flynn | Pending |
| Data quality assessment | Document completeness, duplicate rates, match rate, and outliers | Harlow | Pending |
| Workflow documentation | Document end-to-end pipeline steps for reproducibility | Harlow | Pending |
| Exploratory analysis | Correlation analysis, vote count distribution, decade-level trends | Both | Pending |
| Metadata & data dictionary | Write column definitions and provenance notes | Harlow | Pending |
| Final report | Compile and write full project report in Markdown | Both | Pending |

---

## Constraints

- **Title matching:** Movie titles may differ slightly between datasets (e.g., punctuation, articles, foreign titles). Normalized matching will not resolve all mismatches, reducing the effective size of the merged dataset. This is documented as a known data quality limitation.
- **Popularity metric opacity:** TMDB's `popularity` score is a proprietary composite metric that changes over time. It represents a snapshot rather than a fixed historical value, which limits longitudinal comparisons.
- **Missing critic score values:** Some rows in `movie_info.csv` have missing `critic_score` values, particularly for older films. These will be excluded from correlation analysis but documented in the quality assessment.
- **Genre analysis excluded:** TMDB returns genre data as integer codes without a straightforward label mapping in the basic API response. Genre-level analysis has been excluded from scope to avoid introducing a poorly documented derived variable.
- **API rate limits:** TMDB enforces rate limits (~40 requests/10 seconds). A `time.sleep(0.25)` delay is included in the fetch script to remain compliant.

---

## Gaps and Open Questions

- The best strategy for handling duplicate movie entries in the RT dataset (e.g., *The Aristocats* appears multiple times) has not yet been finalized and will be addressed during the cleaning phase.
- TMDB's `popularity` scoring methodology is not fully publicly documented; this will be noted as a transparency limitation in the data quality section.
- If the match rate after title normalization is lower than expected, the TMDB fetch target may be expanded beyond 500 records.
- A potential stretch goal is pulling additional detail from TMDB's `/movie/{id}` endpoint (e.g., budget, revenue) to further contextualize popularity as a dependent variable.
