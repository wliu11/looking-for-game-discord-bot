import requests

RAIDERIO_API_URL = "https://raider.io/api/v1/characters/profile"

def fetch_character_profile(region: str, realm: str, name: str):
    params = {
        "region": region.lower(),
        "realm": realm.lower(),
        "name": name.lower(),
        "fields": "mythic_plus_scores_by_season:current,mythic_plus_best_runs"
    }

    response = requests.get(RAIDERIO_API_URL, params=params, timeout=10)

    if response.status_code == 404:
        raise ValueError("Character not found")

    response.raise_for_status()
    return response.json()

def extract_mplus_score(data, season):
    seasons = data.get("mythic_plus_scores_by_season", [])

    for s in seasons:
        if s["season"] == season:
            return s["scores"]["all"]

    return None