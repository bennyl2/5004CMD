from dask.distributed import Client
import dask.dataframe as dd
import multiprocessing as mp
import time

CsvPath = r"C:\Users\Leo\Desktop\Uni Year 2\5004CMD\Trips_by_Distance (1).csv"

#reads only bits we need from CSV file
def LoadTrips(Path: str):
    UseCols  = ["Date", "Number of Trips 10-25", "Number of Trips 50-100"]
    DTypeMap = {"Date": "object",
                "Number of Trips 10-25": "float64",
                "Number of Trips 50-100": "float64"}
    Frame = dd.read_csv(Path, usecols=UseCols, dtype=DTypeMap,
                        assume_missing=True, blocksize="32MB")
    Frame["Date"] = dd.to_datetime(Frame["Date"], errors="coerce")
    return Frame

#filters rows with > 10M strips
def Question(TripsByDistance):
    Set1 = TripsByDistance[TripsByDistance["Number of Trips 10-25"] > 10_000_000]
    Set2 = TripsByDistance[TripsByDistance["Number of Trips 50-100"] > 10_000_000]
    Set1.compute(); Set2.compute()

#runs test with 10 processors and then 20
def Benchmark():
    NProcessors = [10, 20]
    Times = {}
    for Proc in NProcessors:
        with Client(n_workers=Proc):
            Trips = LoadTrips(CsvPath)
            Start = time.time()
            Question(Trips)
            Times[Proc] = time.time() - Start
            print(f"{Proc} processors → {Times[Proc]:.2f}s")
    print("All timings:", Times)

if __name__ == "__main__":
    mp.freeze_support()   #windows safety
    Benchmark()