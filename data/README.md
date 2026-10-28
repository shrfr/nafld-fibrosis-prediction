# Data

**File:** `NAFLD.xlsx`
**Dataset:** Kaggle, "Non-alcohol fatty liver disease (NAFLD)"

- Source URL: `<paste the Kaggle dataset URL here>`
- Licence: `<paste the licence shown on the Kaggle dataset page here>`
- Authors / citation: `<paste the authors and paper listed on the Kaggle page here>`

The file is redistributed here only because the licence above permits it. If you reuse this repository, check that licence and cite the original authors.

## Contents

- 605 patients, 62 columns, biopsy-confirmed NAFLD (no healthy controls).
- Only `Sheet1` contains data. `Sheet2` and `Sheet3` are empty.
- Column 0 is `Patient No.` (an ID). Columns 1 to 50 are inputs (demographics, body measures, laboratory values, comorbidities). Columns 51 to 61 are liver biopsy results and derived flags, which must never be used as model inputs.
- Coding: gender Female = 1, Male = 2; most yes/no columns No = 0, Yes = 1.
- Original column spellings (for example `Diyabetes Mellitus`, `Trombosit`) are kept as in the source file.

## Loading

The notebooks read the file directly from this repository:

```
https://raw.githubusercontent.com/shrfr/nafld-fibrosis-prediction/main/data/NAFLD.xlsx
```

(or from `data/NAFLD.xlsx` when the repository is cloned).
