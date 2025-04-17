import warnings
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

#this ignores data format warning
warnings.filterwarnings(
    "ignore",
    message="Could not infer format, so each element will be parsed individually",
    category=UserWarning,
)

DistDf = pd.read_csv(r"C:\Users\Leo\Desktop\Uni Year 2\5004CMD\Trips_by_Distance (1).csv")
FullDf = pd.read_csv(r"C:\Users\Leo\Desktop\Uni Year 2\5004CMD\Trips_Full Data (2).csv")

#removes any invisible spaces that may be sitting at the very start or very end of the text
DistDf.columns = DistDf.columns.str.strip()
FullDf.columns = FullDf.columns.str.strip()

#helps to find column names by keywords
def FindCol(df, *Needles):
    Needles = [n.lower() for n in Needles]
    for Col in df.columns:
        S = Col.lower().replace("  ", " ")
        if all(n in S for n in Needles):
            return Col
    raise KeyError(Needles)  # if we didn’t find anything

#gets required column names
WeekColDist = FindCol(DistDf, "week")
WeekColFull = FindCol(FullDf, "week")
XCol        = FindCol(FullDf, "trips", "1-25", "miles")
YCol        = FindCol(DistDf, "number", "trips", "5-10")

#converts week into week numbers
def ToWeek(Col):
    if np.issubdtype(Col.dtype, np.number):
        return Col.astype("Int64")

    Dt = pd.to_datetime(Col, errors="coerce", format="%Y-%m-%d")
    Wk = Dt.dt.isocalendar().week.astype("Int64")

    Wk[Wk.isna()] = Col[Wk.isna()].astype(str).str.extract(r"(\d{1,2})")[0].astype("Int64")
    return Wk

#add a new WeekKey column in each dataframe
FullDf["WeekKey"] = ToWeek(FullDf[WeekColFull])
DistDf["WeekKey"] = ToWeek(DistDf[WeekColDist])

#merges two files on WeekKey
MergeDf = (
    FullDf[["WeekKey", XCol]]
    .merge(DistDf[["WeekKey", YCol]], on="WeekKey", how="inner")
    .dropna(subset=[XCol, YCol])# removes rows with missing data
)

#builds linear regression model
XModel = MergeDf[[XCol]].to_numpy()
YModel = MergeDf[[YCol]].to_numpy()

Model  = LinearRegression().fit(XModel, YModel)
YPred  = Model.predict(XModel)

#plots points and fitted line
plt.figure(figsize=(8,5))
plt.scatter(XModel, YModel, label="Actual", alpha=0.5)
plt.plot(XModel, YPred,  label="LinearFit", linewidth=2)
plt.xlabel("Trips 1–25 Miles")
plt.ylabel("Number of Trips 5–10")
plt.title("Weekly Trip Frequency vs Trip Length")
plt.legend()
plt.tight_layout()
plt.show()