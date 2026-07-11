#!/usr/bin/env bash
set -euo pipefail

# Simple pipeline skeleton for Milestone 4 (acquire -> clean -> integrate -> analyze)
# Steps can be expanded; integration/analysis scripts not yet implemented in this fast pass.

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
ROOT_DIR="$SCRIPT_DIR"

# If a .env file exists in the repo root, export its variables (so RT_ZIP_URL, TMDB_API_KEY can be set there)
if [ -f "$ROOT_DIR/.env" ]; then
  set -a
  . "$ROOT_DIR/.env"
  set +a
fi

RT_RAW="datasets/movie_info.csv"
TMDB_RAW="datasets/tmdb_movies.csv"

echo "Step 0: ensure datasets directory exists"
mkdir -p datasets

echo "Step 1: Check Rotten Tomatoes source"
if [ -n "${RT_ZIP_URL:-}" ]; then
  echo "  RT_ZIP_URL provided; downloading source from $RT_ZIP_URL"
  python3 "$ROOT_DIR/scripts/acquire_rt.py" --url "$RT_ZIP_URL" --out "$RT_RAW" --force || {
    echo "acquire_rt.py failed" >&2
    exit 1
  }
elif [ -f "$RT_RAW" ]; then
  echo "  Found $RT_RAW"
else
  echo "  Warning: $RT_RAW not found. You can set RT_ZIP_URL to a shared zip or place the CSV at $RT_RAW."
fi

echo "Step 2: Acquire TMDB metadata"
python3 "$ROOT_DIR/scripts/acquire_tmdb.py" --rt-csv "$RT_RAW" --out "$TMDB_RAW" || {
  echo "acquire_tmdb.py failed" >&2
  exit 1
}

echo "Step 3: Clean datasets"
python3 "$ROOT_DIR/scripts/clean.py" --rt-raw "$RT_RAW" --tmdb-raw "$TMDB_RAW" || {
  echo "clean.py failed" >&2
  exit 1
}

echo "Step 4: Integrate cleaned datasets"
python3 "$ROOT_DIR/scripts/integrate.py" --rt-clean "datasets/rt_clean.csv" --tmdb-clean "datasets/tmdb_clean.csv" --out "datasets/merged_movies.csv" || {
  echo "integrate.py failed" >&2
  exit 1
}

echo "Step 5: Run exploratory analysis notebook"
if command -v jupyter &> /dev/null; then
  jupyter nbconvert \
    --to notebook \
    --execute \
    --inplace \
    --ExecutePreprocessor.timeout=300 \
    "$ROOT_DIR/analysis.ipynb" || {
    echo "ERROR: analysis notebook execution failed" >&2
    exit 1
  }
  echo "  analysis.ipynb executed successfully."
else
  echo "  WARNING: jupyter not found — skipping notebook execution."
  echo "  To run the analysis manually: jupyter notebook analysis.ipynb"
fi
 
echo ""
echo "============================================"
echo " Pipeline complete."
echo " Output files:"
echo "   datasets/rt_clean.csv"
echo "   datasets/tmdb_clean.csv"
echo "   datasets/merged_movies.csv"
echo "   analysis.ipynb (executed in-place)"
echo "============================================"
