# mkdir -p tml-data && curl -s 'https://stats.tennismylife.org/api/data-files' | jq -r '.files[] | "\(.url)\t\(.name)"' | while IFS=$'\t' read -r url name; do curl -sSL "$url" -o "tml-data/$name"; done

python3 load_tml.py