import pandas as pd

# load dataset
df = pd.read_csv("data/cleaned/september_master.csv")

# preview
print(df.head())

# check structure
print(df.info())