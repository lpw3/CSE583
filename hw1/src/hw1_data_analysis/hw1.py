"""
CSE 583 HW 1: Fremont Bridge Bicycle Count Analysis
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# 1. Read the CSV file into a pandas dataframe
# ---------------------------------------------------------------------------
data_path = os.path.join(os.path.dirname(__file__), "..", "bicycle_data.csv")
df = pd.read_csv(data_path)

# ---------------------------------------------------------------------------
# 2. Column descriptions and data type corrections
#
# Columns:
#   "Date"
#       - Raw string in the format "MM/DD/YYYY HH:MM:SS AM/PM".
#         Should be a datetime type; converted below.
#   "Fremont Bridge Sidewalks, south of N 34th St Total"
#       - Total bicycle crossings for that hour (East + West combined).
#         Should be int.
#   "Fremont Bridge Sidewalks, south of N 34th St Cyclist West Sidewalk"
#       - Bicycles counted on the west sidewalk for that hour. Should be int.
#   "Fremont Bridge Sidewalks, south of N 34th St Cyclist East Sidewalk"
#       - Bicycles counted on the east sidewalk for that hour. Should be int.
#
# ---------------------------------------------------------------------------
df["Date"] = pd.to_datetime(df["Date"], format="%m/%d/%Y %I:%M:%S %p")

# Rename columns to shorter names for readability
df.columns = ["Date", "Total_official", "West", "East"]

# Coerce count columns to numeric (handles any stray strings or empty cells)
df["West"] = pd.to_numeric(df["West"], errors="coerce")
df["East"] = pd.to_numeric(df["East"], errors="coerce")
df["Total_official"] = pd.to_numeric(df["Total_official"], errors="coerce")

# ---------------------------------------------------------------------------
# 3. Add derived columns
# ---------------------------------------------------------------------------
# 3a. Total (East + West) bicycle count
df["Total"] = df["East"] + df["West"]

# 3b. Hour of the day (0-23)
df["Hour"] = df["Date"].dt.hour

# 3c. Year
df["Year"] = df["Date"].dt.year

# ---------------------------------------------------------------------------
# 4. Subset to 2016 data
# ---------------------------------------------------------------------------
df_2016 = df[df["Year"] == 2016].copy()

# ---------------------------------------------------------------------------
# 5. Check for missing data in the 2016 subset
#
# Number of rows with any missing value: 0
# (All hours in 2016 have complete East and West counts in this dataset.)
# ---------------------------------------------------------------------------
missing_count = df_2016[["East", "West", "Total"]].isna().any(axis=1).sum()
# Number of time points with missing data: 0

# Drop rows with NaN totals so they cannot skew aggregations
df_2016 = df_2016.dropna(subset=["Total"])

# ---------------------------------------------------------------------------
# 6. Plot counts by hour of day for 2016 and save as counts_by_hour.png
# ---------------------------------------------------------------------------
hourly_means = df_2016.groupby("Hour")["Total"].mean()

fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(hourly_means.index, hourly_means.values, color="steelblue", edgecolor="white")
ax.set_title("Average Hourly Bicycle Counts on the Fremont Bridge (2016)")
ax.set_xlabel("Hour of Day (0 = midnight)")
ax.set_ylabel("Average Total Bicycle Count")
ax.set_xticks(range(0, 24))
plt.tight_layout()

output_path = os.path.join(os.path.dirname(__file__), "..", "..", "counts_by_hour.png")
plt.savefig(output_path)
plt.close()

# ---------------------------------------------------------------------------
# 7. Determine the busiest hour of the day (on average) in 2016
#
# Busiest hour: 17 (5pm)
# ---------------------------------------------------------------------------
busiest_hour = int(hourly_means.idxmax())
print(f"Busiest hour of the day in 2016: {busiest_hour}:00 ({busiest_hour % 12 or 12} {'AM' if busiest_hour < 12 else 'PM'})")
print(f"Average total count at that hour: {hourly_means[busiest_hour]:.1f}")
