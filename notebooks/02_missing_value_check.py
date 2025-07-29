
def check_missing(df, name):
    print(f"\nMissing values in {name}:")
    print(df.isnull().sum())
