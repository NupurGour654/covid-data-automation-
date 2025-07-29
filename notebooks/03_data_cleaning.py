
from load_data import load_csv
from check_missing import check_missing

files = [
    "day_wise.csv",
    "country_wise_latest.csv",
    "covid_19_clean_complete.csv",
    "full_grouped.csv",
    "worldometer_data.csv"
]

for file in files:
    df = load_csv(file)
    check_missing(df, file)


