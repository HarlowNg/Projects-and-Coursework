#!/usr/bin/env python3
"""Clean Rotten Tomatoes and TMDB raw CSVs and write cleaned outputs.

Usage:
  python scripts/clean.py --rt-raw datasets/movie_info.csv --tmdb-raw datasets/tmdb_movies.csv
"""
import argparse
import os
import re
import pandas as pd


def normalize_title(title):
    if pd.isna(title):
        return None
    t = str(title).strip().lower()
    t = re.sub(r"[^\w\s]", "", t)
    t = re.sub(r"\s+", " ", t)
    return t.strip()


def extract_year(val):
    if pd.isna(val):
        return None
    m = re.search(r"\b(19|20)\d{2}\b", str(val))
    return int(m.group()) if m else None


def clean_rt(rt_raw_path, rt_out_path):
    rt_df = pd.read_csv(rt_raw_path)

    rt_df["critic_score"] = pd.to_numeric(
        rt_df["critic_score"].astype(str).str.replace('%', '', regex=False), errors='coerce'
    )
    rt_df["audience_score"] = pd.to_numeric(
        rt_df["audience_score"].astype(str).str.replace('%', '', regex=False), errors='coerce'
    )

    rt_df["release_year"] = rt_df["release_date"].apply(extract_year)
    rt_df["title_clean"] = rt_df["title"].apply(normalize_title)

    before = len(rt_df)
    rt_clean = rt_df.dropna(subset=["critic_score", "release_year", "title_clean"]).copy()
    print(f"RT rows dropped (missing values): {before - len(rt_clean)}")

    before_dedup = len(rt_clean)
    rt_clean = rt_clean.sort_values("critic_score", ascending=False)
    rt_clean = rt_clean.drop_duplicates(subset=["title_clean", "release_year"], keep="first")
    print(f"RT rows dropped (duplicates): {before_dedup - len(rt_clean)}")
    print(f"RT clean shape: {rt_clean.shape}")

    os.makedirs(os.path.dirname(rt_out_path) or "datasets", exist_ok=True)
    rt_clean.to_csv(rt_out_path, index=False)
    return rt_clean


def clean_tmdb(tmdb_raw_path, tmdb_out_path):
    tmdb_df = pd.read_csv(tmdb_raw_path)
    tmdb_df["release_year"] = pd.to_datetime(tmdb_df.get("release_date", pd.Series([])), errors='coerce').dt.year
    tmdb_df["title_clean"] = tmdb_df["title"].apply(normalize_title)

    before = len(tmdb_df)
    tmdb_clean = tmdb_df.dropna(subset=["title_clean", "release_year", "popularity"]).copy()
    print(f"TMDB rows dropped (missing values): {before - len(tmdb_clean)}")

    before_dedup = len(tmdb_clean)
    tmdb_clean = tmdb_clean.drop_duplicates(subset=["id"], keep="first")
    print(f"TMDB rows dropped (duplicate IDs): {before_dedup - len(tmdb_clean)}")
    print(f"TMDB clean shape: {tmdb_clean.shape}")

    os.makedirs(os.path.dirname(tmdb_out_path) or "datasets", exist_ok=True)
    tmdb_clean.to_csv(tmdb_out_path, index=False)
    return tmdb_clean


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--rt-raw", default="datasets/movie_info.csv")
    parser.add_argument("--tmdb-raw", default="datasets/tmdb_movies.csv")
    parser.add_argument("--rt-out", default="datasets/rt_clean.csv")
    parser.add_argument("--tmdb-out", default="datasets/tmdb_clean.csv")
    args = parser.parse_args()

    if not os.path.exists(args.rt_raw):
        raise SystemExit(f"RT raw file not found: {args.rt_raw}")
    if not os.path.exists(args.tmdb_raw):
        raise SystemExit(f"TMDB raw file not found: {args.tmdb_raw}")

    rt_clean = clean_rt(args.rt_raw, args.rt_out)
    tmdb_clean = clean_tmdb(args.tmdb_raw, args.tmdb_out)

    print(f"Saved {args.rt_out} ({len(rt_clean)} rows)")
    print(f"Saved {args.tmdb_out} ({len(tmdb_clean)} rows)")


if __name__ == "__main__":
    main()
