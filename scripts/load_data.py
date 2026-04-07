import pandas as pd         #used for data analysis
import sqlite3              #create and interact with database
from pathlib import Path    #helps build file paths safely

#location of python script and builds path to CSV file and database file
file_path = Path(__file__).resolve().parents[1] / "data" / "cleaned" / "september_master.csv"
db_path = Path(__file__).resolve().parents[1] / "data" / "fyeo.db"

#load data
df = pd.read_csv(file_path)

#preview data (first 5)
print(df.head())

#check structure / shows columns
print(df.info())

#clean data
df = df[df["inquiry_count"] > 0].copy()

#formats and removes extra spaces
df["inquiry_topic"] = df["inquiry_topic"].str.strip()
df["category"] = df["category"].str.strip()
df["delivery_method"] = df["delivery_method"].str.strip()

#ensure its numeric format
df["inquiry_count"] = df["inquiry_count"].astype(int)

#ensures its date format
df["inquiry_date"] = pd.to_datetime(df["inquiry_date"])

#checks for any column with missing values
print("\nMissing values:")
print(df.isnull().sum())

#counts for duplicate rows
print("\nDuplicate rows:", df.duplicated().sum())

#adds all inquiry counts
print("Total inquiries:", df["inquiry_count"].sum())

#data analysis - 1 group rows by topic, 2 sum inquiry counts per topic, 3 sort highest, 4 head top 10 topics
print("\nTop topics:")
print(
    df.groupby("inquiry_topic", as_index=False)["inquiry_count"]
      .sum()
      .sort_values("inquiry_count", ascending=False)
      .head(10)
)

#load into database fyeo.db
conn = sqlite3.connect(db_path)

df.to_sql("inquiries", conn, if_exists="replace", index=False)
conn.close()    #closes database connection

#shows how many were loaded / confirmation
print(f"\nLoaded {len(df)} rows into {db_path}")