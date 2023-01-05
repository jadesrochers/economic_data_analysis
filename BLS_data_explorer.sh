# Get all survey data and see what is out there
curl -X GET -o BLS_surveys.json -L "https://api.bls.gov/publicAPI/v2/surveys"
# Single survey data
curl -X GET -o BLS_surveys_AP_consumerPriceData.json -L "https://api.bls.gov/publicAPI/v2/surveys/AP"

# Get 25 most popular time series within a survey
curl -X GET -o BLS_surveys_CPS_consumerPriceData.json -L "https://api.bls.gov/publicAPI/v2/timeseries/popular?survey=AP"
# 25 Most popular from LF/LN 
# labor stats from Current Population Survey (CPS)
curl -X GET -o BLS_survey_LN_LaborForceStats_from_CPS.json -L "https://api.bls.gov/publicAPI/v2/timeseries/popular?survey=LN"

# Getting all data at once, then filtering:
## https://download.bls.gov/pub/time.series/
# Has all time series (I think). You can download and extract what you need
# from the complete csv files.

## Get the series for a specific survey - this is not their api, it
# is just a direct request:
curl -X GET -o BLS_surveys_AP_series.txt -L "https://download.bls.gov/pub/time.series/ap/ap.series"
curl -X GET -o BLS_surveys_AP_area_codes.txt -L "https://download.bls.gov/pub/time.series/ap/ap.area"

# Getting data in xlsx format
# curl -X POST -o dldata.json -L "https://api.bls.gov/publicAPI/v2/timeseries/data.xlsx/?registrationkey=525f29f0b0514e04aee57cd2458939ad&startyear=${startyears[i]}&endyear=${endyears[i]}" -H 'Content-Type: application/json' -d "{\"seriesid\":[\"${seriesid}\"], \"startyear\":\"${startyears[$i]}\", \"endyear\":\"${endyears[$i]}\", \"registrationkey\":\"525f29f0b0514e04aee57cd2458939ad\" }"

# Getting data from the api in json format.
# curl -X POST -o testdata.json -L 'https://api.bls.gov/publicAPI/v2/timeseries/data/?registrationkey=525f29f0b0514e04aee57cd2458939ad&startyear=1950&endyear=1969' -H 'Content-Type: application/json' -d '{"seriesid":["LNU02300000"], "startyear":"1950", "endyear":"1969", "registrationkey":"525f29f0b0514e04aee57cd2458939ad" }'

