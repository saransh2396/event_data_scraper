# =============================================================================
# config.py
# All league URLs, file paths, and scraping settings in one place.
# To scrape a different league, just change ACTIVE_LEAGUE below.
# =============================================================================

# ── League URLs ───────────────────────────────────────────────────────────────
LEAGUE_URLS = {
    "EPL":          "https://www.scoresway.com/en_GB/soccer/premier-league-2026-2027/6pdwluctev9iebv00r4qqukno/results",
    "LA_LIGA":      "https://www.scoresway.com/en_GB/soccer/primera-divisi%C3%B3n-2026-2027/830epggffy1nfkfyrtpqdwhlg/results",
    "SERIE_A":      "https://www.scoresway.com/en_GB/soccer/serie-a-2026-2027/60cryos85i4bp5ul34tt0brx0/results",
    "BUNDESLIGA":   "https://www.scoresway.com/en_GB/soccer/bundesliga-2026-2027/8h5xijv2u4mlf5028gso6kw7o/results",
    "LIGUE_1":      "https://www.scoresway.com/en_GB/soccer/ligue-1-2026-2027/bqnc4ccgnrp6pb3bktqet0yz8/results",
    "PRIMEIRA_LIGA":"https://www.scoresway.com/en_GB/soccer/primeira-liga-2025-2026/7l4z25o4hc0fmj9rdspcisdn8/results",
    "ISL":          "https://www.scoresway.com/en_GB/soccer/indian-super-league-2026-2027/2whe9kz3el4ir50k7cp55p3bo/results",
}

# ── Active league (change this to switch leagues) ─────────────────────────────
ACTIVE_LEAGUE = "LA_LIGA"
ACTIVE_URL    = LEAGUE_URLS[ACTIVE_LEAGUE]

# ── How many recent matchweeks to scrape (0 = most recent) ───────────────────
MATCHWEEKS_TO_SCRAPE = 12

# ── Output directory (use raw string for Windows paths) ───────────────────────
OUTPUT_DIRS = {
    "EPL":          r"D:\Leagues Data\League data\Scoresway\2026_27_Season\EPL_scoresway_2026_27",
    "LA_LIGA":      r"D:\Leagues Data\League data\Scoresway\2026_27_Season\La_Liga_scoresway_2026_27",
    "SERIE_A":      r"D:\Leagues Data\League data\Scoresway\2026_27_Season\SerieA_scoresway_2026_27",
    "BUNDESLIGA":   r"D:\Leagues Data\League data\Scoresway\2026_27_Season\Bundesliga_scoresway_2026_27",
    "LIGUE_1":      r"D:\Leagues Data\League data\Scoresway\2026_27_Season\Ligue_1_scoresway_2026_27",
    "PRIMEIRA_LIGA":r"D:\Leagues Data\League data\Scoresway\2025_26_Season\PrimeiraLiga_scoresway_2025_26",
    "ISL":          r"D:\Leagues Data\League data\Scoresway\2026_27_Season\ISL_scoresway_2026_27",

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
