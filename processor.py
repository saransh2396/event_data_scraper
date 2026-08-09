# =============================================================================
# processor.py
# Fetches match event data from a player-stats URL and saves it as .xlsx.
# All DataFrame building, column mapping, and file I/O lives here.
# =============================================================================

import os
import pandas as pd
import numpy as np
import DataFrameGetter as dfg

import config


def _load_opta_references() -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Load Opta event-type and qualifier lookup tables from CSV.
    Returns (type_id_df, qualifiers_df).
    """
    type_id_df = pd.read_csv(config.OPTA_EVENTS_CSV, encoding="ISO-8859-1")
    type_id_df.rename(columns={"ID": "typeId"}, inplace=True)

    qualifiers_df = pd.read_csv(config.OPTA_QUALIFIERS_CSV)

    return type_id_df, qualifiers_df


def _build_output_path(match_info: dict) -> tuple[str, str]:
    """
    Derive the output filename and full file path from matchInfo.
    Returns (file_name, full_file_path).
    """
    contestants = match_info["contestant"]
    home = next(
        x["officialName"].replace(" ", "_")
        for x in contestants if x.get("position") == "home"
    )
    away = next(
        x["officialName"].replace(" ", "_")
        for x in contestants if x.get("position") == "away"
    )
    date_str = match_info["localDate"].replace("-", "_")
    file_name = f"{date_str}_{home}_vs_{away}.xlsx"
    full_path = os.path.join(config.OUTPUT_DIR, file_name)
    return file_name, full_path


def _build_events_dataframe(content_element: dict, type_id_df: pd.DataFrame, qualifiers_df: pd.DataFrame) -> pd.DataFrame:
    """
    Build and enrich the events DataFrame from the API response content element.
    Returns the processed events_df.
    """
    teams_df = pd.DataFrame(content_element["matchInfo"]["contestant"])
    events_df = pd.DataFrame(content_element["liveData"]["event"])

    id1    = teams_df["id"].iloc[0]
    team1  = teams_df["officialName"].iloc[0]
    id2    = teams_df["id"].iloc[1]
    team2  = teams_df["officialName"].iloc[1]

    # Map contestant IDs to team names
    events_df["contestantId"] = np.where(events_df["contestantId"] == id1, team1, team2)

    # Map outcome codes to labels
    events_df["outcome"] = np.where(events_df["outcome"] == 1, "Successful", "Unsuccessful")

    # Rename columns to readable names
    events_df.rename(columns={
        "contestantId": "Team",
        "timeMin":      "Minute",
        "timeSec":      "Seconds",
    }, inplace=True)

    # Add event description and qualifier columns
    event_action_result = events_df.apply(
        dfg.return_event_data_and_description, args=(type_id_df,), axis=1
    )
    events_df["typeId"], events_df["Description"] = zip(*event_action_result)
    events_df["qualifier"] = events_df.apply(
        dfg.return_qualifier_data, args=(qualifiers_df,), axis=1
    )

    return events_df


def process_and_save(url: str) -> bool:
    """
    Fetch event data for a single match URL, build the DataFrame, and save as .xlsx.

    Returns True on success, False on failure.
    """
    try:
        response     = dfg.fetch_event_response(url)
        match_info   = response["matchevent"]["response_content"]["matchInfo"]
        file_name, full_path = _build_output_path(match_info)

        if os.path.exists(full_path):
            print(f"  Already exists, skipping: {file_name}")
            return True

        type_id_df, qualifiers_df = _load_opta_references()

        content_element = response["matchevent"]["response_content"]
        events_df = _build_events_dataframe(content_element, type_id_df, qualifiers_df)

        os.makedirs(config.OUTPUT_DIR, exist_ok=True)
        events_df.to_excel(full_path, index=False)
        print(f"  Saved: {file_name}")
        return True

    except Exception as e:
        print(f"  Error processing {url}: {type(e).__name__}: {e}")
        return False


def process_all_urls(all_urls: list[str]) -> list[str]:
    """
    Process and save every URL in all_urls.

    Returns a list of URLs that failed (for retry / inspection).
    """
    failed_urls: list[str] = []
    total = len(all_urls)

    for idx, url in enumerate(all_urls, start=1):
        print(f"\n[{idx}/{total}] {url}")
        success = process_and_save(url)
        if not success:
            failed_urls.append(url)

    print(f"\n── Summary ──────────────────────────────────────────")
    print(f"  Total  : {total}")
    print(f"  Saved  : {total - len(failed_urls)}")
    print(f"  Failed : {len(failed_urls)}")
    if failed_urls:
        print("  Failed URLs:")
        for u in failed_urls:
            print(f"    {u}")

    return failed_urls
