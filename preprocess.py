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

        # Attempt to extract RSU ID from folder name
        rsu_id = None
        if rsu_folder.startswith("RSU_"):
            rsu_id_str = rsu_folder.split("_")[1]
        elif rsu_folder.startswith("RSU-"):
            rsu_id_str = rsu_folder.split("-")[1]
        else:
            print(f"Skipping folder '{rsu_folder}' as it doesn't match the expected pattern.")
            continue

        try:
            rsu_id = int(rsu_id_str)
        except ValueError:
            print(f"Warning: Unable to convert RSU ID '{rsu_id_str}' to integer. Skipping folder: {rsu_folder}")
            continue

        for csv_file in glob.glob(os.path.join(full_path, "run_*.csv")):
            run_filename = os.path.basename(csv_file)
            run_parts = run_filename.split("_")
            if len(run_parts) < 2:
                print(f"Skipping file '{csv_file}' due to unexpected naming format.")
                continue
            run_id_str = run_parts[1].split(".")[0]
            try:
                run_id = int(run_id_str)
            except ValueError:
                print(f"Warning: Unable to convert run ID '{run_id_str}' to integer. Skipping file: {csv_file}")
                continue
            df = pd.read_csv(csv_file)
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
