import pandas as pd
import matplotlib.pyplot as plt

Cols        = ['Level', 'Date', 'Number of Trips 10-25', 'Number of Trips 50-100']
BigDataset  = pd.read_csv(r"C:\Users\Leo\Desktop\Uni Year 2\5004CMD\Trips_by_Distance (1).csv",
                          usecols=Cols)
BigDataset.columns = BigDataset.columns.str.strip()   #removes spaces

#keep only national rows and the two trip columns
NationalOnly = BigDataset[BigDataset['Level'] == 'National'][
               ['Date', 'Number of Trips 10-25', 'Number of Trips 50-100']]

#filters to > 10M trips only
Cond10 = NationalOnly['Number of Trips 10-25'] > 10_000_000
Cond50 = NationalOnly['Number of Trips 50-100'] > 10_000_000

Set1 = NationalOnly[Cond10]
Set2 = NationalOnly[Cond50]
Set3 = NationalOnly[Cond10 & Cond50]
Set4 = NationalOnly[Cond10 & ~Cond50]

print(len(Set1), len(Set2), len(Set3), len(Set4))

#scatter plots
Plots = [
    ('Set 1: Trips 10‑25 > 10 M', Set1, 'Number of Trips 10-25'),
    ('Set 2: Trips 50‑100 > 10 M', Set2, 'Number of Trips 50-100'),
    ('Set 3: Both Conditions',     Set3, 'Number of Trips 50-100'),
    ('Set 4: Only Trips 10‑25 > 10 M', Set4, 'Number of Trips 50-100')
]

for Title, Data, YLabel in Plots:
    plt.figure()
    plt.scatter(pd.to_datetime(Data['Date']), Data[YLabel], alpha=0.5)
    plt.title(Title)
    plt.xlabel('Date')
    plt.ylabel(YLabel)
    plt.xticks(rotation=45)
    plt.tight_layout()

plt.show()