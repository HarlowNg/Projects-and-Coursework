#!/usr/bin/env python3
"""Download Rotten Tomatoes dataset (zip or csv) and extract `movie_info.csv`.

Supports Google Drive share links and direct HTTP(S) links. Writes to `datasets/movie_info.csv` by default.

Usage:
  python scripts/acquire_rt.py --url <URL> --out datasets/movie_info.csv
"""
import argparse
import os
import re
import sys
import tempfile
import shutil
import zipfile
import json
from urllib.parse import urlparse, parse_qs

import requests
import pandas as pd


def ensure_datasets_dir(path):
    d = os.path.dirname(path) or "datasets"
    os.makedirs(d, exist_ok=True)


def extract_drive_id(url):
    # patterns: /d/<id>/ or id=<id>
    m = re.search(r"/d/([A-Za-z0-9_-]+)", url)
    if m:
        return m.group(1)
    qs = parse_qs(urlparse(url).query)
    if "id" in qs:
        return qs["id"][0]
    return None


def get_confirm_token(response):
    for key, val in response.cookies.items():
        if key.startswith("download_warning"):
            return val
    m = re.search(r"confirm=([0-9A-Za-z_]+)&", response.text)
    if m:
        return m.group(1)
    return None


def save_response_content(response, destination):
    CHUNK_SIZE = 32768
    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:
                f.write(chunk)


def download_from_google_drive(file_id, destination):
    session = requests.Session()
    URL = "https://docs.google.com/uc?export=download"
    response = session.get(URL, params={"id": file_id}, stream=True)
    token = get_confirm_token(response)
    if token:
        response = session.get(URL, params={"id": file_id, "confirm": token}, stream=True)
    response.raise_for_status()
    save_response_content(response, destination)


def download_http(url, destination, timeout=30):
    resp = requests.get(url, stream=True, timeout=timeout)
    resp.raise_for_status()
    save_response_content(resp, destination)


def choose_member_from_zip(zf, prefer_name="movie_info.csv"):
    names = [n for n in zf.namelist() if not n.endswith('/')]
    # exact match
    for n in names:
        if os.path.basename(n) == prefer_name:
            return n
    # any csv
    for n in names:
        if n.lower().endswith('.csv'):
            return n
    # any json
    for n in names:
        if n.lower().endswith('.json'):
            return n
    return None


def extract_csv_from_zip(zip_path, out_path):
    with zipfile.ZipFile(zip_path, 'r') as zf:
        member = choose_member_from_zip(zf)
        if not member:
            raise RuntimeError("No CSV/JSON member found in zip archive")
        basename = os.path.basename(member)
        if basename.lower().endswith('.csv'):
            zf.extract(member, path=os.path.dirname(out_path) or '.')
            src = os.path.join(os.path.dirname(out_path) or '.', member)
            shutil.move(src, out_path)
        else:
            # JSON -> convert to CSV
            with zf.open(member) as fh:
                data = json.load(fh)
            df = pd.DataFrame(data)
            df.to_csv(out_path, index=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', required=True, help='HTTP(S) or Google Drive share URL pointing to zip/csv/json')
    parser.add_argument('--out', default='datasets/movie_info.csv', help='Output CSV path')
    parser.add_argument('--force', action='store_true', help='Overwrite existing output')
    args = parser.parse_args()

    if os.path.exists(args.out) and not args.force:
        print(f"Output {args.out} already exists. Use --force to overwrite.")
        sys.exit(0)

    ensure_datasets_dir(args.out)

    url = args.url.strip()
    tmp = tempfile.NamedTemporaryFile(delete=False)
    tmp.close()
    try:
        if 'drive.google.com' in url or 'docs.google.com' in url:
            file_id = extract_drive_id(url)
            if not file_id:
                raise SystemExit("Could not extract Google Drive file ID from URL")
            print("Downloading from Google Drive file id:", file_id)
            download_from_google_drive(file_id, tmp.name)
        else:
            print("Downloading from URL:", url)
            download_http(url, tmp.name)

        # If downloaded file is a zip, extract
        if zipfile.is_zipfile(tmp.name):
            print("Downloaded zip archive, extracting CSV...")
            extract_csv_from_zip(tmp.name, args.out)
        else:
            # Not a zip. Try to detect JSON or CSV by content or extension
            lower = url.lower()
            if lower.endswith('.csv'):
                shutil.move(tmp.name, args.out)
            elif lower.endswith('.json'):
                print('Converting JSON to CSV')
                with open(tmp.name, 'r') as fh:
                    data = json.load(fh)
                df = pd.DataFrame(data)
                df.to_csv(args.out, index=False)
            else:
                # Try inspect first bytes
                with open(tmp.name, 'rb') as fh:
                    start = fh.read(2048)
                text = None
                try:
                    text = start.decode('utf-8', errors='ignore')
                except Exception:
                    pass
                if text and text.lstrip().startswith('{'):
                    with open(tmp.name, 'r') as fh:
                        data = json.load(fh)
                    df = pd.DataFrame(data)
                    df.to_csv(args.out, index=False)
                else:
                    # Assume CSV
                    shutil.move(tmp.name, args.out)

        print(f"Saved Rotten Tomatoes CSV to {args.out}")
    finally:
        try:
            if os.path.exists(tmp.name):
                os.remove(tmp.name)
        except Exception:
            pass


if __name__ == '__main__':
    main()
