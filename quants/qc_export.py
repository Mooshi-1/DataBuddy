

#get data in this format

import pandas as pd

# Storing data as a list of dictionaries
data = [
    {"drug name": "morphine", "area counts": 6000000, "retention time": "0.23 min", "concentration": "0.03 mg/L"},
    {"drug name": "codeine", "area counts": 7000000, "retention time": "2.5 min", "concentration": "0.10 mg/L"},
    # Add more entries as needed
]

# Converting to DataFrame
df = pd.DataFrame(data)

# Exporting to Excel
df.to_excel('CaseNumber_results.xlsx', index=False)
