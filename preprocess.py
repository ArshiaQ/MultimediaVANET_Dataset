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
        for csv_file in glob.glob(os.path.join(full_path, "run_*.csv")):
            df = pd.read_csv(csv_file)
            # Extract information from folder and file names
            rsu_id_str = rsu_folder.split("_")[1]
            run_id_str = os.path.basename(csv_file).split("_")[1].split(".")[0]
            try:
                rsu_id = int(rsu_id_str)
            except ValueError:
                print(f"Warning: Unable to convert RSU ID '{rsu_id_str}' to integer. Skipping file: {csv_file}")
                continue
            try:
                run_id = int(run_id_str)
            except ValueError:
                print(f"Warning: Unable to convert run ID '{run_id_str}' to integer. Skipping file: {csv_file}")
                continue
            df["RSU_id"] = rsu_id
            df["run_id"] = run_id
            dfs.append(df)
    if dfs:
        return pd.concat(dfs, ignore_index=True)
    else:
        return pd.DataFrame()  # Return an empty DataFrame if no valid data was found

def main():
    combined = load_and_label()
    if not combined.empty:
        combined.to_csv(OUTPUT_FILE, index=False)
        print(f"[✔] Combined dataset saved to {OUTPUT_FILE}")
        print(combined.head())
    else:
        print("No valid data found to combine.")

if __name__ == "__main__":
    main()
