import os
import numpy as np
import pandas as pd

# === تنظیمات ===
OUTPUT_DIR = "data"
RSU_IDS     = [1,2,3,4]
DURATION_S  = 120       # طول شبیه‌سازی بر حسب ثانیه
STEP_S      = 1         # گام زمانی
MEANS       = {
    "throughput": 50,   # Mbps
    "delay": 10,        # ms
    "jitter": 1,        # ms
    "loss": 0.5         # درصد
}
STDS        = {
    "throughput": 3,
    "delay": 2,
    "jitter": 0.2,
    "loss": 0.2
}

def generate_run(rsu_id, run_id):
    """دیتای مصنوعی برای یک RSU در یک run خاص"""
    times = np.arange(0, DURATION_S+1, STEP_S)
    df = pd.DataFrame({
        "time_s": times,
        f"throughput_RSU{rsu_id}_Mbps": np.random.normal(MEANS["throughput"], STDS["throughput"], len(times)).round(2),
        f"e2e_delay_ms": np.random.normal(MEANS["delay"], STDS["delay"], len(times)).round(2),
        f"jitter_ms": np.random.normal(MEANS["jitter"], STDS["jitter"], len(times)).round(3),
        f"packet_loss_pct": np.clip(np.random.normal(MEANS["loss"], STDS["loss"], len(times)), 0, 100).round(2),
    })
    return df

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for rsu in RSU_IDS:
        rsu_dir = os.path.join(OUTPUT_DIR, f"RSU_{rsu:02d}")
        os.makedirs(rsu_dir, exist_ok=True)
        # چند run مختلف
        for run in range(3):
            df = generate_run(rsu, run)
            file_path = os.path.join(rsu_dir, f"run_{run:03d}.csv")
            df.to_csv(file_path, index=False)
            print(f"[✔] Saved {file_path}")

if __name__ == "__main__":
    main()
