#!/usr/bin/env python3
"""Merge cleaned Rotten Tomatoes and TMDB datasets into a single merged CSV.

Usage:
  python scripts/integrate.py --rt-clean datasets/rt_clean.csv --tmdb-clean datasets/tmdb_clean.csv --out datasets/merged_movies.csv
"""
import argparse
import os
import sys
import pandas as pd


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--rt-clean', default='datasets/rt_clean.csv', help='Path to RT cleaned CSV')
    parser.add_argument('--tmdb-clean', default='datasets/tmdb_clean.csv', help='Path to TMDB cleaned CSV')
    parser.add_argument('--out', default='datasets/merged_movies.csv', help='Output merged CSV path')
    args = parser.parse_args()

    if not os.path.exists(args.rt_clean):
        print(f'RT clean file not found: {args.rt_clean}', file=sys.stderr)
        sys.exit(2)
    if not os.path.exists(args.tmdb_clean):
        print(f'TMDB clean file not found: {args.tmdb_clean}', file=sys.stderr)
        sys.exit(3)

    rt_df = pd.read_csv(args.rt_clean)
    tmdb_df = pd.read_csv(args.tmdb_clean)

    # Select TMDB columns to bring into the merged dataset (same as notebook)
    tmdb_cols = ['title_clean', 'release_year', 'id', 'popularity', 'vote_count', 'vote_average', 'overview']
    tmdb_available = [c for c in tmdb_cols if c in tmdb_df.columns]
    if set(tmdb_cols) - set(tmdb_available):
        print(f'Warning: missing TMDB columns: {set(tmdb_cols) - set(tmdb_available)}')

    tmdb_subset = tmdb_df[tmdb_available].copy()

    merged_df = pd.merge(
        rt_df,
        tmdb_subset,
        on=['title_clean', 'release_year'],
        how='inner'
    )

    print(f'Merged shape: {merged_df.shape}')
    if len(tmdb_df) > 0:
        print(f'Match rate vs TMDB clean:  {len(merged_df) / len(tmdb_df) * 100:.1f}%')

    print('Missing values in merged dataset:')
    print(merged_df.isnull().sum())

    # Drop rows with any missing values to provide a clean dataset for analysis
    before_drop = len(merged_df)
    merged_df = merged_df.dropna()
    dropped = before_drop - len(merged_df)
    if dropped > 0:
        print(f'Rows dropped due to missing values: {dropped}')
    print(f'Final merged shape after dropping missing: {merged_df.shape}')

    os.makedirs(os.path.dirname(args.out) or 'datasets', exist_ok=True)
    merged_df.to_csv(args.out, index=False)
    print(f'Wrote {len(merged_df)} rows to {args.out}')


if __name__ == '__main__':
    main()
