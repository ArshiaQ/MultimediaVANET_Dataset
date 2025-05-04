# Multimedia VANET Dataset

این مخزن شامل داده‌های شبیه‌سازی‌شده برای پروژه‌ی ارتباطات چندرسانه‌ای با VANET و 5G NR است.

## ساختار

- `data/RSU_##/run_XXX.csv`  
  هر پوشه مربوط به یک RSU است و هر فایل یک Run مجزا.

- `simulate_data.py`  
  تولید داده‌ی مصنوعی یا تبدیل خروجی SUMO+NS-3 به CSV.

- `preprocess.py`  
  ادغام تمام CSVها در یک دیتاست واحد `combined_dataset.csv`.

- `metadata.csv`  
  مشخصات آماری پارامترها (میانگین و انحراف معیار).

## استفاده

1. نصب وابستگی‌ها  
   ```bash
   pip install -r requirements.txt
