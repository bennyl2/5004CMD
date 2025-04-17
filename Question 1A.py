import pandas as pd
import dask.dataframe as dd
import matplotlib.pyplot as plt

#datasets stored
SmallDataset = pd.read_csv(r"C:\Users\Leo\Desktop\Uni Year 2\5004CMD\Trips_by_Distance (1).csv")
BigDataset = dd.read_csv(r"C:\Users\Leo\Desktop\Uni Year 2\5004CMD\Trips_Full Data (2).csv")

#filtering national level data
NationalOnly = BigDataset[BigDataset['Level'] == "National"]

#location bases columns become NaN
NationalOnly = NationalOnly.drop(columns=['State FIPS', 'State Postal Code', 'County FIPS', 'County Name'], errors='ignore')

#filter small dataset by data range
NationalOnly = NationalOnly[NationalOnly["Date"].between(SmallDataset['Date'].min(), SmallDataset['Date'].max())]

#converst date to datetime
NationalOnly['Date'] = dd.to_datetime(NationalOnly['Date'], errors='coerce')

#get week number
NationalOnly['Week'] = NationalOnly['Date'].dt.strftime('%U').astype(int)

#group weeks and gets average
WeeklyData = NationalOnly.groupby('Week')[[
    'Population Staying at Home',
    'People Not Staying at Home',
    'Trips 1-25 Miles',
    'Trips 25-100 Miles',
    'Trips 100+ Miles'
]].mean().compute().reset_index()

#dataframes for plots
GroupedData = WeeklyData[['Week', 'Population Staying at Home']]
GroupedDataTwo = WeeklyData[['Week', 'People Not Staying at Home']]

#people staying at home:
plt.figure(figsize=(10, 5))
plt.bar(GroupedData['Week'], GroupedData['Population Staying at Home'], color='skyblue')
plt.xlabel('Week')
plt.ylabel('Population Staying at Home')
plt.title('Average Population Staying at Home per Week')
plt.xticks(GroupedData['Week'], rotation=45)
plt.tight_layout()
plt.show()

#people not staying at home
plt.figure(figsize=(10, 5))
plt.bar(GroupedDataTwo['Week'], GroupedDataTwo['People Not Staying at Home'], color='skyblue')
plt.xlabel('Week')
plt.ylabel('Population Not Staying at Home')
plt.title('Average Population Not Staying at Home per Week')
plt.xticks(GroupedDataTwo['Week'], rotation=45)
plt.tight_layout()
plt.show()

#mean trips by distance range
AdditionData = WeeklyData[['Trips 1-25 Miles', 'Trips 25-100 Miles', 'Trips 100+ Miles']].mean()

plt.figure(figsize=(8, 5))
AdditionData.plot(kind='bar', color='orange')
plt.xlabel('Distance Ranges')
plt.ylabel('Mean Trips')
plt.title('Histogram of Mean Trips by Distance Ranges')
plt.tight_layout()
plt.savefig("Histogram of Mean Trips by Distance Ranges.png")
plt.show()