import requests
import requests_mock
from utils.raiderio_api import fetch_character_profile

def test_fetch_character_profile():

    mock_response = {
        "name": "Sicilia",
        "class": "Evoker",
        "realm": "Illidan",
        "region": "us",
        "mythic_plus_scores_by_season": [
            {
                "season": "season-mn-1",
                "scores": {
                    "all": 3125.4
                }
            }
        ]
    }

    with requests_mock.Mocker() as m:
        m.get(
            "https://raider.io/api/v1/characters/profile",
            json=mock_response
        )

        data = fetch_character_profile("us", "illidan", "Sicilia")

        assert data["name"] == "Sicilia"
        assert data["class"] == "Evoker"

from utils.raiderio_api import extract_mplus_score

def test_extract_score():
    mock_data = {
        "mythic_plus_scores_by_season": [
            {
                "season": "season-mn-1",
                "scores": {
                    "all": 2500
                }
            }
        ]
    }

    score = extract_mplus_score(mock_data, "season-mn-1")

    assert score == 2500