#!/bin/bash

Dataset=$1
# Dataset=CAINC1
Region=$2
# Region=NY
Years=All
Format=JSON
UserToken=74B6144A-CFBF-48F9-9A6E-F50213F7FA39

# Get available linecodes for a dataset
# This may (or may not) be specific to the Regional dataset
get_linecodes() {
    tablename="$1"
    local filename="tmp_BEA_linecodes.json"
    curl -X GET -o "$filename" -L "http://apps.bea.gov/api/data?UserID=${UserToken}&method=GetParameterValues&datasetname=Regional&ParameterName=LineCode&ResultFormat=${Format}" 
    linecodes=$(jq < tmp_BEA_linecodes.json | grep -C 1 -i "$tablename" | grep -i key | sed 's/"//g' | sed -r 's/[^0-9]*([0-9]+).*/\1/' | uniq)
    rm "$filename"
    printf '%s\n' "$linecodes"
}

get_data_and_metadata() {
    set -x
    tablename="$1"
    linecode="$2"
    local dl_filename="tmp_BEA_datameta_${tablename}_${linecode}.json"
    local csv_filename="dl_BEA_${tablename}_fulltable.csv"
    curl -X GET -o "${dl_filename}" -L "http://apps.bea.gov/api/data?UserID=74B6144A-CFBF-48F9-9A6E-F50213F7FA39&method=GetData&datasetname=Regional&GeoFips=${Region}&TableName=${tablename}&LineCode=${linecode}&Year=${Years}&ResultFormat=${Format}"
    jq -r '["GeoFips", "GeoName", "TimePeriod", .BEAAPI.Results.Data[0].Code], (.BEAAPI.Results.Data | sort_by(.GeoFips,.TimePeriod)[] | [.GeoFips,.GeoName,.TimePeriod,.DataValue]) | @csv' < "$dl_filename" > "$csv_filename"
    rm "$dl_filename"
    printf '%s' "$csv_filename"
    set +x
}

append_more_data() {
    tablename="$1"
    linecode="$2"
    base_csv="$3"
    local dl_filename="tmp_BEA_data_${tablename}_${linecode}.json"
    local csv_filename="dl_BEA_${tablename}_datatable.csv"
    local new_filename="dl_BEA_${tablename}_fulltable_${linecode}.csv"
    curl -X GET -o "${dl_filename}" -L "http://apps.bea.gov/api/data?UserID=${UserToken}&method=GetData&datasetname=Regional&GeoFips=${Region}&TableName=${tablename}&LineCode=${linecode}&Year=${Years}&ResultFormat=${Format}"
    jq -r '[.BEAAPI.Results.Data[0].Code], (.BEAAPI.Results.Data | sort_by(.GeoFips,.TimePeriod)[] | [.DataValue]) | @csv' < "$dl_filename" > "$csv_filename"
    paste -d ',' "$base_csv" "$csv_filename" > "$new_filename"
    rm "$dl_filename" "$csv_filename" "$base_csv"
    printf "%s" "$new_filename" 
}



LineCodes=($(get_linecodes "$Dataset"))
n=0
basefilename=''
for linecode in ${LineCodes[@]}: do
    local basefilename
    if n -eq 0; then
        basefilename=$(get_data_and_metadata "$Dataset" "$linecode")
    else
        basefilename=$(append_more_data "$Dataset" "$linecode" "$basefilename")
        n=((n+1))
done

