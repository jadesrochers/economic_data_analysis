#!/bin/bash

# Raw means I download the raw text data files and transform them to 
# something else, usually csv format or similar for easy python use.
## This is Different from the other BLS downloader because it uses
# the URL for direct downloads, does not bother with the api.

# Get all survey data and see what is out there
curl -X GET -o BLS_surveys.json -L "https://api.bls.gov/publicAPI/v2/surveys"

# The only argument specifies whether to download all the raw data
getdata=$1

if [[ "$getdata" == true ]]; then
    ## Looking at the LN series - Labor force statistics at national level
    curl -X GET -o BLS_LaborForceStats_LN_series.txt -L "https://download.bls.gov/pub/time.series/ln/ln.series"
    # Get all the data - about 350 Mb
    curl -X GET -o BLS_LaborForceStats_LN_data_ALL.txt -L "https://download.bls.gov/pub/time.series/ln/ln.data.1.AllData"
fi

# Get a limited set of sub-series to look at - Monthly, and not too specific
# grep -E '^[A-Z0-9]+[0]{4,}.*M.*(Seas).*[Pp]articipation' < BLS_LaborForceStats_LN_series.txt
# grep -E '^[A-Z0-9]+[0]{5,}.*M.*(Seas).*[Uu]nemployment' < BLS_LaborForceStats_LN_series.txt

## And extract the series ids from those 
participationRateSeries=$(grep -E '^[A-Z0-9]+[0]{4,}.*M.*(Seas).*[Pp]articipation Rate' < BLS_LaborForceStats_LN_series.txt | awk '{print $1}')
unemploymentRateSeries=$(grep -E '^[A-Z0-9]+[0]{5,}.*M.*(Seas).*[Uu]nemployment Rate' < BLS_LaborForceStats_LN_series.txt | awk '{print $1}')
unemploymentLevelSeries=$(grep -E '^[A-Z0-9]+[0]{5,}.*M.*(Seas).*[Uu]nemployment Level' < BLS_LaborForceStats_LN_series.txt | awk '{print $1}')

## Narrow the text file down to just the target series to 
# make things faster on the Python side:
rm BLS_LN_Rate_Series.txt BLS_LN_Level_Series.txt
touch BLS_LN_Rate_Series.txt BLS_LN_Level_Series.txt
for series in ${participationRateSeries[@]}; do
   grep -E "^${series}\s" <BLS_LaborForceStats_LN_data_ALL.txt >>BLS_LN_Rate_Series.txt
done
for series in ${unemploymentRateSeries[@]}; do
   grep -E "^${series}\s" <BLS_LaborForceStats_LN_data_ALL.txt >>BLS_LN_Rate_Series.txt
done
for series in ${unemploymentLevelSeries[@]}; do
   grep -E "^${series}\s" <BLS_LaborForceStats_LN_data_ALL.txt >>BLS_LN_Level_Series.txt
done

# Convert from space separated to comman separated
sed -i.back -r 's/\s+$//g; s/\s+/,/g;' BLS_LN_Rate_Series.txt
sed -i.back -r 's/\s+$//g; s/\s+/,/g;' BLS_LN_Level_Series.txt

