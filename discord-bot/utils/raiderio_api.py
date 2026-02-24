import requests

RAIDERIO_API_URL = "https://raider.io/api/v1/characters/profile"

def fetch_character_profile(region: str, realm: str, name: str):
    params = {
        "region": region,
        "realm": realm,
        "name": name,
        "fields": "mythic_plus_scores_by_season"
    }

    response = requests.get(RAIDERIO_API_URL, params=params, timeout=10)

    if response.status_code == 404:
        raise ValueError("Character not found")

    response.raise_for_status()
    return response.json()
