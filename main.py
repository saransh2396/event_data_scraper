# =============================================================================
# main.py
# Entry point — run this file in PyCharm to start the scrape.
#
# Flow:
#   1. Read config (league, matchweeks to scrape, output dir)
#   2. Scrape player-stats URLs for the N most recent matchweeks
#   3. Process each URL → build events DataFrame → save as .xlsx
# =============================================================================

import config
import scraper
import processor


def main():
    print("=" * 60)
    print(f"  Scoresway Scraper")
    print(f"  League  : {config.ACTIVE_LEAGUE}")
    print(f"  URL     : {config.ACTIVE_URL}")
    print(f"  Weeks   : last {config.MATCHWEEKS_TO_SCRAPE} matchweeks")
    print(f"  Output  : {config.OUTPUT_DIR}")
    print("=" * 60)

    # ── Step 1: Optional — check total matchweeks available ──────────────────
    print("\n[Step 1] Checking total matchweeks available...")
    total_matchweeks = scraper.get_total_matchweeks(config.ACTIVE_URL)
    print(f"  Total matchweeks on site: {total_matchweeks}")

    weeks_to_scrape = min(config.MATCHWEEKS_TO_SCRAPE, total_matchweeks)
    print(f"  Will scrape: {weeks_to_scrape} matchweeks")

    # ── Step 2: Collect all player-stats URLs ─────────────────────────────────
    print("\n[Step 2] Collecting player-stats URLs...")
    mw_url_map = scraper.collect_all_urls(config.ACTIVE_URL, weeks_to_scrape)

    # Flatten all matchweek URL lists into one list, preserving every URL.
    # Do NOT deduplicate here — each matchweek is a separate set of real matches.
    # The only safe dedup is inside process_and_save(), which skips files that
    # already exist on disk (so re-running is always safe).
    all_urls = [url for urls in mw_url_map.values() for url in urls]
    print(f"\n  Total URLs collected: {len(all_urls)} across {len(mw_url_map)} matchweeks")

    if not all_urls:
        print("  No URLs found — exiting.")
        return

    # ── Step 3: Fetch event data and save as .xlsx ────────────────────────────
    print("\n[Step 3] Processing and saving match event data...")
    failed_urls = processor.process_all_urls(all_urls)

    print("\n[Done]")
    if failed_urls:
        print(f"  {len(failed_urls)} URL(s) failed. Re-run or inspect manually.")


if __name__ == "__main__":
    main()
