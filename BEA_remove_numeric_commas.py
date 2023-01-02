import pandas as pd
import numpy as np
import re
import sys

print('Args: ', sys.argv)
inputname=sys.argv[1]
outputname=sys.argv[2]
print('Input: {input}, Output: {Output}'.format(input=inputname, output=outputname))
# filename='dl_BEA_CAINC1_fulltable_3.csv'

num = re.compile('[",0-9]+')
income_df = pd.read_csv(inputname)


for colname in income_df.columns:
    if income_df.dtypes[colname] == 'object':
        match_prop = sum(income_df.apply(lambda row: 1 if num.match(row[colname]) else 0, axis=1)) / len(income_df[colname])
        if match_prop > 0.9:
            income_df[colname] = income_df[colname].apply(lambda x: int(x.replace(',', '')))

# income_df.to_csv('BEA_CAINC1_converted.csv')
income_df.to_csv(outputname)

## sed command that could mostly do the same thing:
# sed -r 's/([0-9]),([0-9])/\1\2/g' dl_BEA_CAINC1_fulltable_3.csv
