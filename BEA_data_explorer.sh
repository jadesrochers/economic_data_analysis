# Get the major top level data sets
curl -X GET -o dl_bea_datasetlist.json -L "http://apps.bea.gov/api/data?UserID=74B6144A-CFBF-48F9-9A6E-F50213F7FA39&method=getDataList&ResultFormat=JSON"
# Get the parameters that can be passed to one of those top level sets
curl -X GET -o dl_bea_dataset_parameters.json -L "http://apps.bea.gov/api/data?UserID=74B6144A-CFBF-48F9-9A6E-F50213F7FA39&method=getParameterList&datasetname=Regional&ResultFormat=JSON"

## Getting the specific arguments allowable to a parameter for a set; 
# because there are several arguments to any given set, be aware that
# arguments to one parameter may be valid only in combination with other args
curl -X GET -o dl_bea_dataset_Regional_LineCodes.json -L "http://apps.bea.gov/api/data?UserID=74B6144A-CFBF-48F9-9A6E-F50213F7FA39&method=GetParameterValues&datasetname=Regional&ParameterName=LineCode&ResultFormat=JSON"
# Get the specific tables available:
curl -X GET -o dl_bea_dataset_Regional_TableNames.json -L "http://apps.bea.gov/api/data?UserID=74B6144A-CFBF-48F9-9A6E-F50213F7FA39&method=GetParameterValues&datasetname=Regional&ParameterName=TableName&ResultFormat=JSON"

# Get nice pretty print of the result
jq -C < dl_bea_dataset_parameter_args.json

## Now get the data (only one field at a time, disappointing):
curl -X GET -o dl_bea_dataset_CAINC1.json -L "http://apps.bea.gov/api/data?UserID=74B6144A-CFBF-48F9-9A6E-F50213F7FA39&method=GetData&datasetname=Regional&GeoFips=NY&TableName=CAINC1&LineCode=1,2,3&Year=All&ResultFormat=JSON"
## Get a different field - checkout out what is feasible to get
curl -X GET -o dl_bea_dataset_CAINC1_92.json -L "http://apps.bea.gov/api/data?UserID=74B6144A-CFBF-48F9-9A6E-F50213F7FA39&method=GetData&datasetname=Regional&GeoFips=NY&TableName=CAINC1&LineCode=92&Year=All&ResultFormat=JSON"


