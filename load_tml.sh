#!/usr/bin/env bash

set -euo pipefail

rm -rf tml-data && mkdir -p tml-data

curl -fsS 'https://stats.tennismylife.org/api/data-files' | jq -r '.files[] | "\(.url)\t\(.name)"' | while IFS=$'\t' read -r url name; do curl -fsSL "$url" -o "tml-data/$name"; done

python3 load_tml.py