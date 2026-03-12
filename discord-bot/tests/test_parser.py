from utils.raiderio_parser import parse_raiderio_character_url

def test_parse_raiderio_url():
    url = "https://raider.io/characters/us/illidan/Sicilia"

    result = parse_raiderio_character_url(url)

    assert result["region"] == "us"
    assert result["realm"] == "illidan"
    assert result["name"] == "Sicilia"