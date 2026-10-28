# Notebooks

| File | Purpose | Owner |
|---|---|---|
| `setup_cell.py` | The shared setup cell. Paste it into the first cell of every notebook and run it first | all |
| `01_eda.ipynb` | Steps 1 to 6: data inspection, targets, leakage, missingness, feature ranking, FIB-4 benchmark | EDA |
| `02_modeling.ipynb` | Step 7 onward: split, pipeline, models, comparison, tuning, SHAP, secondary experiments | modeling |

Tips:

- Use **Runtime > Restart and run all** before saving, so the stored outputs match the code.
- Work in your own notebook file to avoid merge conflicts, since notebooks are hard to merge.
- Do not store keys or tokens in any cell.
