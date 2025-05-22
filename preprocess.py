import os
import glob
import pandas as pd

DATA_DIR = "data"
OUTPUT_FILE = "combined_dataset.csv"

def load_and_label():
    dfs = []
    for rsu_folder in sorted(os.listdir(DATA_DIR)):
        full_path = os.path.join(DATA_DIR, rsu_folder)
        if not os.path.isdir(full_path):
            continue
        if "_" not in rsu_folder:
            print(f"Skipping folder '{rsu_folder}' as it doesn't match the expected pattern.")
            continue
        rsu_parts = rsu_folder.split("_")
        if len(rsu_parts) < 2:
            print(f"Skipping folder '{rsu_folder}' due to unexpected format.")
            continue
        rsu_id = rsu_parts[1]
        for csv_file in glob.glob(os.path.join(full_path, "run_*.csv")):
            df = pd.read_csv(csv_file)
            run_id = os.path.basename(csv_file).split("_")[1].split(".")[0]
            df["RSU_id"] = int(rsu_id)
            df["run_id"] = int(run_id)
            dfs.append(df)
    return pd.concat(dfs, ignore_index=True)

def main():
    combined = load_and_label()
    combined.to_csv(OUTPUT_FILE, index=False)
    print(f"[✔] Combined dataset saved to {OUTPUT_FILE}")
    print(combined.head())

if __name__ == "__main__":
    main()
