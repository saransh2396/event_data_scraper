# =============================================================================
# config.py
# All league URLs, file paths, and scraping settings in one place.
# To scrape a different league, just change ACTIVE_LEAGUE below.
# =============================================================================

# ── League URLs ───────────────────────────────────────────────────────────────
LEAGUE_URLS = {
    "EPL":          "https://www.scoresway.com/en_GB/soccer/premier-league-2025-2026/51r6ph2woavlbbpk8f29nynf8/results",
    "LA_LIGA":      "https://www.scoresway.com/en_GB/soccer/primera-división-2025-2026/80zg2v1cuqcfhphn56u4qpyqc/results",
    "SERIE_A":      "https://www.scoresway.com/en_GB/soccer/serie-a-2025-2026/emdmtfr1v8rey2qru3xzfwges/results",
    "BUNDESLIGA":   "https://www.scoresway.com/en_GB/soccer/bundesliga-2025-2026/2bchmrj23l9u42d68ntcekob8/results",
    "LIGUE_1":      "https://www.scoresway.com/en_GB/soccer/ligue-1-2025-2026/dbxs75cag7zyip5re0ppsanmc/results",
    "PRIMEIRA_LIGA":"https://www.scoresway.com/en_GB/soccer/primeira-liga-2025-2026/7l4z25o4hc0fmj9rdspcisdn8/results",
    "ISL":          "https://www.scoresway.com/en_GB/soccer/indian-super-league-2025-2026/d70h9cciplfhf01fn96gpcw0k/results",
    "FIFA_World_Cup":"https://www.scoresway.com/en_GB/soccer/fifa-world-cup-2026-canada-mexico-usa/873cbl9cd9butm4air0mugxzo/results"
}

# ── Active league (change this to switch leagues) ─────────────────────────────
ACTIVE_LEAGUE = "EPL"
ACTIVE_URL    = LEAGUE_URLS[ACTIVE_LEAGUE]

# ── How many recent matchweeks to scrape (0 = most recent) ───────────────────
MATCHWEEKS_TO_SCRAPE = 38

# ── Output directory (use raw string for Windows paths) ───────────────────────
OUTPUT_DIRS = {
    "EPL":          r"D:\Leagues Data\League data\Scoresway\2025_26_Season\EPL_scoresway_2025_26",
    "LA_LIGA":      r"D:\Leagues Data\League data\Scoresway\2025_26_Season\La_Liga_scoresway_2025_26",
    "SERIE_A":      r"D:\Leagues Data\League data\Scoresway\2025_26_Season\SerieA_scoresway_2025_26",
    "BUNDESLIGA":   r"D:\Leagues Data\League data\Scoresway\2025_26_Season\Bundesliga_scoresway_2025_26",
    "LIGUE_1":      r"D:\Leagues Data\League data\Scoresway\2025_26_Season\Ligue_1_scoresway_2025_26",
    "PRIMEIRA_LIGA":r"D:\Leagues Data\League data\Scoresway\2025_26_Season\PrimeiraLiga_scoresway_2025_26",
    "ISL":          r"D:\Leagues Data\League data\Scoresway\2025_26_Season\ISL_scoresway_2025_26",
    "FIFA_World_Cup": r"D:\Leagues Data\League data\Scoresway\FIFA_World_Cup"
}
OUTPUT_DIR = OUTPUT_DIRS[ACTIVE_LEAGUE]

# ── Opta reference data paths ─────────────────────────────────────────────────
OPTA_EVENTS_CSV     = r"./opta_data/template/opta-events.csv"
OPTA_QUALIFIERS_CSV = r"./opta_data/template/opta-qualifiers.csv"

# ── Selenium / timing settings ────────────────────────────────────────────────
DRIVER_IMPLICIT_WAIT  = 10    # seconds
DRIVER_LOAD_SLEEP     = 5     # seconds to wait after driver.get()
EXPLICIT_WAIT_TIMEOUT = 20    # seconds for WebDriverWait
OVERLAY_SETTLE_SLEEP  = 2     # seconds to let page re-inject overlays before removing them
