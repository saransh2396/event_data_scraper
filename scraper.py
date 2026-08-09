# =============================================================================
# scraper.py
# Scoresway-specific scraping logic.
# Responsible for: counting matchweeks, collecting player-stats URLs per game.
# Returns plain data (lists/dicts) — no file I/O, no DataFrame work here.
# =============================================================================

from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from time import sleep

import config
import browser


# ── CSS selectors used across this module ─────────────────────────────────────
SEL_DROPDOWN_BTN  = ".Opta-Exp"
SEL_DROPDOWN_LIST = "ul.Opta-Cf"
SEL_FIXTURE_ROW   = "tbody.Opta-result.Opta-fixture"
SEL_VIEW_MATCH    = '[title="View match"]'
SEL_STRIPLIST     = "ul.striplist"


def get_total_matchweeks(url: str) -> int:
    """
    Open the results page, expand the matchweek dropdown,
    and return the total number of matchweek entries.
    """
    driver = browser.get_driver(url)
    try:
        browser.remove_cookie_dialog(driver)
        sleep(1)

        clicker = browser.wait_for(driver, SEL_DROPDOWN_BTN)
        browser.js_click(driver, clicker)

        ul_element = browser.wait_for(driver, SEL_DROPDOWN_LIST)
        count = len(ul_element.find_elements(By.TAG_NAME, "li"))
        return count
    finally:
        driver.quit()


def _expand_matchweek_dropdown(driver, wait_timeout: int = 10):
    """
    Remove overlays, then expand the matchweek dropdown.
    Returns the list of <a> elements inside the dropdown.
    """
    sleep(config.OVERLAY_SETTLE_SLEEP)
    browser.remove_cookie_dialog(driver)
    sleep(0.5)

    clicker = browser.wait_for(driver, SEL_DROPDOWN_BTN, timeout=wait_timeout)
    browser.js_click(driver, clicker)

    ul_element = browser.wait_for(driver, SEL_DROPDOWN_LIST, timeout=wait_timeout)
    return ul_element.find_elements(By.TAG_NAME, "a")


def _collect_player_stats_url(driver, fixture_index: int, matchweek_name: str):
    """
    Given a loaded fixtures page, click the fixture at fixture_index,
    find the PLAYER STATS tab link, then navigate back.
    Returns the URL string, or None if not found.
    """
    # Re-fetch fixture list fresh (avoids StaleElementReferenceException)
    fixture_tables = [
        x for x in driver.find_elements(By.CSS_SELECTOR, SEL_FIXTURE_ROW)
        if x.text
    ]

    if fixture_index >= len(fixture_tables):
        print(f"    [{matchweek_name}] Game {fixture_index + 1}: index out of range after reload, skipping")
        return None

    fixture = fixture_tables[fixture_index]
    match_page = fixture.find_element(By.CSS_SELECTOR, SEL_VIEW_MATCH)
    browser.js_click(driver, match_page)
    browser.remove_cookie_dialog(driver)

    striplist = browser.wait_for(driver, SEL_STRIPLIST)
    result_urls = [
        x.find_element(By.TAG_NAME, "a").get_property("href")
        for x in striplist.find_elements(By.TAG_NAME, "li")
        if x.text.strip() == "PLAYER STATS"
    ]

    # Navigate back to fixture list
    driver.execute_script("window.history.go(-1)")
    browser.wait_for(driver, SEL_FIXTURE_ROW)

    return result_urls[0] if result_urls else None


def scrape_matchweek_urls(url: str, matchweek_index: int):
    """
    Scrape all player-stats URLs for a single matchweek.

    Args:
        url:              The main results page URL.
        matchweek_index:  0 = most recent matchweek, 1 = one before, etc.

    Returns:
        (matchweek_name, list_of_player_stats_urls)
    """
    driver = browser.get_driver(url)
    browser.remove_cookie_dialog(driver)

    name = f"Matchweek_{matchweek_index}"
    urls = []

    try:
        all_mw = _expand_matchweek_dropdown(driver)

        if len(all_mw) <= matchweek_index:
            print(f"  [Index {matchweek_index}] Overflow — no more matchweeks available")
            return name, urls

        mw_item = all_mw[matchweek_index]
        name = mw_item.text.strip() or f"Matchweek_{matchweek_index}"
        print(f"  Scraping matchweek {matchweek_index}: '{name}'")

        browser.js_click(driver, mw_item)
        browser.wait_for(driver, SEL_FIXTURE_ROW)

        # Count fixtures before entering the loop
        num_fixtures = len([
            x for x in driver.find_elements(By.CSS_SELECTOR, SEL_FIXTURE_ROW)
            if x.text
        ])
        print(f"    Found {num_fixtures} fixtures")

        for j in range(num_fixtures):
            try:
                print(f"    Game {j + 1}/{num_fixtures} ...", end=" ")
                player_stats_url = _collect_player_stats_url(driver, j, name)

                if player_stats_url:
                    urls.append(player_stats_url)
                    print(f"OK → {player_stats_url}")
                else:
                    print("No PLAYER STATS link found")

            except StaleElementReferenceException as e:
                print(f"StaleElement — skipping: {e}")
                try:
                    driver.execute_script("window.history.go(-1)")
                    browser.wait_for(driver, SEL_FIXTURE_ROW)
                except Exception:
                    pass
                continue

            except Exception as e:
                print(f"Error ({type(e).__name__}) — skipping: {e}")
                try:
                    driver.execute_script("window.history.go(-1)")
                    browser.wait_for(driver, SEL_FIXTURE_ROW)
                except Exception:
                    pass
                continue

    except Exception as e:
        print(f"  Fatal error on matchweek {matchweek_index}: {type(e).__name__}: {e}")

    finally:
        driver.quit()

    return name, urls


def collect_all_urls(url: str, num_matchweeks: int):
    """
    Scrape player-stats URLs for the most recent `num_matchweeks` matchweeks.

    Returns:
        {"0_Matchday 33": [...], "1_Playoff": [...], "2_Playoff": [...], ...}

    FIX: Keys are prefixed with the matchweek index so duplicate display names
    (e.g. multiple rounds all labelled 'Playoff') never overwrite each other
    in the results dict — which was silently losing 10 URLs per collision.
    """
    results = {}
    failed = []

    for i in range(num_matchweeks):
        print(f"\n[Matchweek index {i}]")
        try:
            name, urls = scrape_matchweek_urls(url, i)
            # Prefix index to key — guarantees uniqueness even when site
            # returns the same label for multiple matchweeks (e.g. "Playoff")
            unique_key = f"{i}_{name}"
            results[unique_key] = urls
            print(f"  → Collected {len(urls)} URLs for '{name}'")
        except Exception as e:
            print(f"  Unhandled error for matchweek index {i}: {e}")
            failed.append(i)

    if failed:
        print(f"\nFailed matchweek indices: {failed}")

    total = sum(len(v) for v in results.values())
    print(f"\n  Total URLs across all matchweeks: {total}")

    return results
