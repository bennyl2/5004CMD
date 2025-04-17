import warnings
import dask.dataframe as dd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler

warnings.filterwarnings("ignore", category=UserWarning)  #ignore warning

PathSmall = r"C:\Users\Leo\Desktop\Uni Year 2\5004CMD\Trips_by_Distance (1).csv"
PathBig   = r"C:\Users\Leo\Desktop\Uni Year 2\5004CMD\Trips_Full Data (2).csv"

TextCols = {"County Name": "object", "State Postal Code": "object"}

SmallDs = dd.read_csv(PathSmall, dtype=TextCols, assume_missing=True)
BigDs   = dd.read_csv(PathBig,   dtype=TextCols, assume_missing=True)

#keep national rows only
NationalOnly = BigDs[BigDs["Level"] == "National"]

#matches date range of two files
StartDate = SmallDs["Date"].min().compute()
EndDate   = SmallDs["Date"].max().compute()

Merged = (
    NationalOnly[NationalOnly["Date"].between(StartDate, EndDate)]
    .compute()
)

#removes hidden spaces in column names
Merged.columns = Merged.columns.str.strip()

#pick columns by name
XCol = "Trips 1-25 Miles"
YCol = "Trips 5-10 Miles"

XRaw = Merged[[XCol]].to_numpy()
YRaw = Merged[[YCol]].to_numpy()

#scales axes as previously lines weren't showing due to miscaling
Sx, Sy = StandardScaler(), StandardScaler()
X = Sx.fit_transform(XRaw)
Y = Sy.fit_transform(YRaw)

Model = LinearRegression().fit(X, Y)
print(f"R²: {Model.score(X, Y):.3f}")

#predictions and plot
YPred = Model.predict(X)

plt.figure(figsize=(8, 5))
plt.scatter(X, Y, alpha=0.6, label="Actual")
plt.plot(X, YPred, color="red", linewidth=2, label="Linear Fit")
plt.xlabel("Trips 1–25 Miles (scaled)")
plt.ylabel("Trips 5–10 Miles (scaled)")
plt.title("Linear Regression – Weekly Trip Frequency vs Trip Length")
plt.legend()
plt.tight_layout()
plt.show()