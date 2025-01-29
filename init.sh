#!/usr/bin/env bash
set -e

echo "Running IMDb import script..."

cd /app

pg_ctl -o "-c listen_addresses='localhost' \
           -c log_min_messages=fatal \
           -c max_wal_size=2GB" -w restart

python3 -m imdblib all

echo "IMDb import script completed."
