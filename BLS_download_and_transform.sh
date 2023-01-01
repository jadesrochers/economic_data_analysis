#!/bin/bash

# You can get multiple series, but it seems only 20 years of data at once
# Not great given that 12 obs in a year is typical - not exactly API breaking to do the full period of record

seriesid='LNU02300000'

echo '' > "${seriesid}.csv"

startyears=(1950 1970 1990 2010)
endyears=(1969 1989 2009 2022)

get_series_data() {
    # for i in {0..${#startyears[@]}}; do
    blocks=${#startyears[@]}
    for (( i=0; i<blocks; i++ )); do
        printf 'Getting years: %s %s\ndata series: %s\n' "${startyears[i]}" "${endyears[i]}" "${seriesid}"
        curl -X POST -o dldata.json -L "https://api.bls.gov/publicAPI/v2/timeseries/data.xlsx/?registrationkey=525f29f0b0514e04aee57cd2458939ad&startyear=${startyears[i]}&endyear=${endyears[i]}" -H 'Content-Type: application/json' -d "{\"seriesid\":[\"${seriesid}\"], \"startyear\":\"${startyears[$i]}\", \"endyear\":\"${endyears[$i]}\", \"registrationkey\":\"525f29f0b0514e04aee57cd2458939ad\" }"
        xlsx2csv -a dldata.xlsx > dldata.csv
        sed -n -r '/^[12][0-9]{3}/,${p}' < dldata.csv | tac >> "${seriesid}.csv"
	sleep 1;
    done
}


## Get the series defined above. Upgrade this to pass as an argument to improve.
# get_series_data 
