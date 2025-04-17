import pandas as pd
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.pyplot as plt

TripsFull = pd.read_csv(r"C:\Users\Leo\Desktop\Uni Year 2\5004CMD\Trips_Full Data (2).csv")

#national only (filtering)
NationalOnly = TripsFull[TripsFull['Level'] == "National"]

#mean trips by distance range
MeanTrips = NationalOnly[['Trips 1-25 Miles', 'Trips 25-100 Miles', 'Trips 100+ Miles']].mean()

#plot
plt.figure(figsize=(8, 5))
MeanTrips.plot(kind='bar', color='green')
plt.xlabel("Distance Ranges")
plt.ylabel("Mean Number of Trips")
plt.title("Number of Travellers by Distance Range")
plt.tight_layout()
plt.savefig("Question1E_TravellerByDistance.png")
plt.show()