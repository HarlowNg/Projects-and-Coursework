#!/usr/bin/env python3
"""Acquire TMDB metadata for titles listed in a Rotten Tomatoes CSV.

Usage:
  python scripts/acquire_tmdb.py --rt-csv datasets/movie_info.csv --out datasets/tmdb_movies.csv

The script reads `TMDB_API_KEY` from the environment or `.env` (via python-dotenv).
"""
import argparse
import os
import time
import sys
import requests
import pandas as pd
from dotenv import load_dotenv


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--rt-csv", default="datasets/movie_info.csv", help="Path to Rotten Tomatoes CSV")
    parser.add_argument("--out", default="datasets/tmdb_movies.csv", help="Output CSV path")
    parser.add_argument("--api-key", default=None, help="TMDB API key (optional, will read from .env)")
    parser.add_argument("--limit", type=int, default=700, help="Maximum number of TMDB records to fetch")
    parser.add_argument("--sleep", type=float, default=0.25, help="Seconds to sleep between requests")
    parser.add_argument("--unique", action="store_true", help="Only query unique titles (keeps first occurrence)")
    args = parser.parse_args()

    load_dotenv()
    api_key = args.api_key or os.getenv("TMDB_API_KEY")
    if not api_key:
        print("Error: TMDB API key not provided. Set TMDB_API_KEY in .env or pass --api-key.")
        sys.exit(2)

    if not os.path.exists(args.rt_csv):
        print(f"Error: input RT CSV not found: {args.rt_csv}")
        sys.exit(3)

    rt_df = pd.read_csv(args.rt_csv)
    titles = rt_df["title"].fillna("").tolist()
    if args.unique:
        seen = set()
        uniq = []
        for t in titles:
            if t not in seen:
                seen.add(t)
                uniq.append(t)
        titles = uniq

    BASE_URL = "https://api.themoviedb.org/3"
    session = requests.Session()

    movies = []
    for i, title in enumerate(titles):
        if len(movies) >= args.limit:
            break
        q = str(title).strip()
        if not q:
            continue

        try:
            resp = session.get(
                f"{BASE_URL}/search/movie",
                params={"api_key": api_key, "query": q, "language": "en-US"},
                timeout=10,
            )
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            print(f"Error querying TMDB for '{q}': {e}")
            time.sleep(1)
            continue

        results = data.get("results", [])
        if results:
            movies.append(results[0])
            print(f"[{len(movies)}/{args.limit}] Found: {q}")
        else:
            print(f"  Skipped (no match): {q}")

        time.sleep(args.sleep)

    df = pd.DataFrame(movies)
    # Ensure expected columns exist
    for col in ["id", "title", "release_date", "vote_average", "vote_count", "popularity", "overview"]:
        if col not in df.columns:
            df[col] = None

    df = df[["id", "title", "release_date", "vote_average", "vote_count", "popularity", "overview"]]

    os.makedirs(os.path.dirname(args.out) or "datasets", exist_ok=True)
    df.to_csv(args.out, index=False)
    print(f"Wrote {len(df)} rows to {args.out}")


if __name__ == "__main__":
    main()
