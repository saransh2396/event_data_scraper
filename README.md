# Scoresway Scraper

Modular PyCharm project that scrapes football match event data from Scoresway and saves it as `.xlsx` files.

---

## Project Structure

```
scoresway_scraper/
│
├── main.py           ← Entry point — run this
├── config.py         ← All settings: league URLs, output paths, timing
├── browser.py        ← Generic Selenium helpers (driver, clicks, waits)
├── scraper.py        ← Scoresway page navigation + URL collection
├── processor.py      ← Fetch event data, build DataFrame, save .xlsx
│
├── DataFrameGetter.py  ← (Your existing module — place here)
│
└── opta_data/
    └── template/
        ├── opta-events.csv
        └── opta-qualifiers.csv
```

---

## Setup

1. Install dependencies:
   ```bash
   pip install selenium beautifulsoup4 requests pandas numpy openpyxl
   ```

2. Make sure `chromedriver` is on your PATH and matches your Chrome version.

3. Place your `DataFrameGetter.py` in the project root.

4. Place `opta-events.csv` and `opta-qualifiers.csv` in `opta_data/template/`.

---

## Configuration (`config.py`)

| Setting | Description |
|---|---|
| `ACTIVE_LEAGUE` | Which league to scrape (`"EPL"`, `"SERIE_A"`, `"LA_LIGA"`, etc.) |
| `MATCHWEEKS_TO_SCRAPE` | How many recent matchweeks to scrape (default: `6`) |
| `OUTPUT_DIR` | Auto-set from `OUTPUT_DIRS[ACTIVE_LEAGUE]` |

To switch league, change one line:
```python
ACTIVE_LEAGUE = "SERIE_A"
```

---

## Running

Open the project in PyCharm and run `main.py`, or from terminal:
```bash
python main.py
```

---

## Module Responsibilities

| Module | Responsibility |
|---|---|
| `config.py` | Constants only — no logic |
| `browser.py` | Generic Selenium: launch driver, remove overlays, JS click, wait |
| `scraper.py` | Scoresway navigation: count matchweeks, collect player-stats URLs |
| `processor.py` | Data pipeline: fetch API response → DataFrame → save `.xlsx` |
| `main.py` | Wires everything together, prints progress |
