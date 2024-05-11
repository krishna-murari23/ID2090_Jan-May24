#!/bin/bash

# Fetch data from the online source
curl -s "https://apod.nasa.gov/apod/archivepixFull.html" > temp.html

data=$(cat temp.html)

datefn() {
	input="$1"
	IFS=' ' read -ra parts <<<"$input"
	num=()
	text_part=""
	for part in "${parts[@]}"; do
		if [[ $part =~ ^[0-9]+$ ]]; then
			num+=("$part")
		else
			text_part="$part"
		fi
	done
	sorted_num=($(printf "%s\n" "${num[@]}" | sort -n))
	rearranged_date="${sorted_num[0]} ${sorted_num[1]} $text_part"
	echo "$rearranged_date"
}

titles=$(echo "$data" | grep -oP '(?<=>).*?(?=<\/a>)')
special_dates_divisible_by_DD=""
special_dates_divisible_by_MM=""

while IFS= read -r line; do
	date=${line%%:*}
	formatted_date=$(dat "$date")
	MM=$(echo "$formatted_date" | awk '{$1=$2=""; print $0}' | sed 's/^[ \t]*//')
	case "$MM" in
		January) MM=1 ;;
		February) MM=2 ;;
		March) MM=3 ;;
		April) MM=4 ;;
		May) MM=5 ;;
		June) MM=6 ;;
		July) MM=7 ;;
		August) MM=8 ;;
		September) MM=9 ;;
		October) MM=10 ;;
		November) MM=11 ;;
		December) MM=12 ;;
	esac
	DD=$(echo "$formatted_date" | awk '{print $1}' | sed 's/^0*//')
	YYYY=$(echo "$formatted_date" | awk '{print $2}')
done <<<"$data"

echo -e "$special_dates_divisible_by_DD" >answer_1a.csv
echo -e "$special_dates_divisible_by_MM" >answer_1b.csv

