# mkdir -p tml-data && curl -s 'https://stats.tennismylife.org/api/data-files' | jq -r '.files[] | "\(.url)\t\(.name)"' | while IFS=$'\t' read -r url name; do curl -sSL "$url" -o "tml-data/$name"; done

sqlite3 tennis_data.db < tennis_schema.sql

# what if tennis_data.db already exists? Am I always copying and replacing with a version from
# repo or adding to a local version? Should I always reset or just add new matches?

python3 load_tml.py