import warnings
import dask.dataframe as dd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler

warnings.filterwarnings("ignore", category=UserWarning)

# ── CSV locations ────────────────────────────────────────────────────
PATH_SMALL = r"C:\Users\Leo\Desktop\Uni Year 2\5004CMD\Trips_by_Distance (1).csv"
PATH_BIG   = r"C:\Users\Leo\Desktop\Uni Year 2\5004CMD\Trips_Full Data (2).csv"

# ── only the trouble‑making columns need explicit dtypes ─────────────
TEXT_COLS = {"County Name": "object", "State Postal Code": "object"}

small_ds = dd.read_csv(PATH_SMALL, dtype=TEXT_COLS, assume_missing=True)
big_ds   = dd.read_csv(PATH_BIG,   dtype=TEXT_COLS, assume_missing=True)

# ── keep national rows only ──────────────────────────────────────────
national_only = big_ds[big_ds["Level"] == "National"]

# ── match the date range of the two files ────────────────────────────
start_date = small_ds["Date"].min().compute()
end_date   = small_ds["Date"].max().compute()

merged = (
    national_only[national_only["Date"].between(start_date, end_date)]
    .compute()
)

# ── strip hidden spaces in column names ──────────────────────────────
merged.columns = merged.columns.str.strip()

# ── pick columns directly by exact names that exist ──────────────────
x_col = "Trips 1-25 Miles"
y_col = "Trips 5-10 Miles"          # <- this column IS present

X_raw = merged[[x_col]].to_numpy()
Y_raw = merged[[y_col]].to_numpy()

# ── scale both axes so line is visible ───────────────────────────────
sx, sy = StandardScaler(), StandardScaler()
X = sx.fit_transform(X_raw)
Y = sy.fit_transform(Y_raw)

model = LinearRegression().fit(X, Y)
print(f"R²: {model.score(X, Y):.3f}")

# ── predictions + plot ───────────────────────────────────────────────
Y_pred = model.predict(X)

plt.figure(figsize=(8, 5))
plt.scatter(X, Y, alpha=0.6, label="Actual")
plt.plot(X, Y_pred, color="red", linewidth=2, label="Linear Fit")
plt.xlabel("Trips 1–25 Miles (scaled)")
plt.ylabel("Trips 5–10 Miles (scaled)")
plt.title("Linear Regression – Weekly Trip Frequency vs Trip Length")
plt.legend()
plt.tight_layout()
plt.show()
