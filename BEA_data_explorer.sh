# Get the major top level data sets
curl -X GET -o dl_bea_datasetlist.json -L "http://apps.bea.gov/api/data?UserID=74B6144A-CFBF-48F9-9A6E-F50213F7FA39&method=getDataSetList&ResultFormat=JSON"
# Get the parameters that can be passed to one of those top level sets
curl -X GET -o dl_bea_dataset_parameters.json -L "http://apps.bea.gov/api/data?UserID=74B6144A-CFBF-48F9-9A6E-F50213F7FA39&method=getParameterList&datasetname=Regional&ResultFormat=JSON"

## Getting the specific arguments allowable to a parameter for a set; 
# because there are several arguments to any given set, be aware that
# arguments to one parameter may be valid only in combination with other args
curl -X GET -o dl_bea_dataset_Regional_LineCodes.json -L "http://apps.bea.gov/api/data?UserID=74B6144A-CFBF-48F9-9A6E-F50213F7FA39&method=GetParameterValues&datasetname=Regional&ParameterName=LineCode&ResultFormat=JSON"
# Get the specific tables available:
curl -X GET -o dl_bea_dataset_Regional_TableNames.json -L "http://apps.bea.gov/api/data?UserID=74B6144A-CFBF-48F9-9A6E-F50213F7FA39&method=GetParameterValues&datasetname=Regional&ParameterName=TableName&ResultFormat=JSON"


##### Short list of abbreviation meanings 
# Becuase there are a ton and it is hard to work out, their documentation
# is hard to find

##### IMPORTANT: Table and LineCode
# The Table is defined by the leading Letters that you will see repeated a lot (CAINC for example)
# and the trailing value (1, 30, 5N, 5S) is the LineCode

### Should start with indicator if this is state or county or something else
# S - State
# C - County
#
### Then the frequency
# A - Annual
# Q - Quarterly 
# M - Monthly
# SQA - Quarterly, seasonally adjusted
# QNSA - Quarterly, non-seasonally adjusted
#
### Then an abbreviation of what the set is about 
# INC - Income
# 

### Full Table Name - 
### The codes above are modified by an id - this can be number, letters
# There are different tables for: (County, Annual, Income)
# CAINC1
# CAINC30
# CAINC4
# CAINC5N
# CAINC5S
### Which contain differing, but also often overlapping data

## Determining Line codes - 
curl -X GET -o dl_bea_linecodes_CAGDP1.json -L "http://apps.bea.gov/api/data?UserID=74B6144A-CFBF-48F9-9A6E-F50213F7FA39&method=GetParameterValuesFiltered&datasetname=Regional&TargetParameter=LineCode&TableName=CAGDP1&ResultFormat=JSON"

# Get nice pretty print of the result
jq -C < dl_bea_dataset_parameter_args.json


## Now get the data (only one field at a time):
curl -X GET -o dl_bea_dataset_CAINC1_2.json -L "http://apps.bea.gov/api/data?UserID=74B6144A-CFBF-48F9-9A6E-F50213F7FA39&method=GetData&datasetname=Regional&GeoFips=NY&TableName=CAINC1&LineCode=2&Year=All&ResultFormat=JSON"

## Get a different field - checkout out what is feasible to get
curl -X GET -o dl_bea_dataset_CAINC1_92.json -L "http://apps.bea.gov/api/data?UserID=74B6144A-CFBF-48F9-9A6E-F50213F7FA39&method=GetData&datasetname=Regional&GeoFips=NY&TableName=CAINC1&LineCode=92&Year=All&ResultFormat=JSON"


