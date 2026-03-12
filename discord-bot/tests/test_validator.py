from utils.raiderio_validator import is_valid_raiderio_character

def test_valid_raiderio_url():
    url = "https://raider.io/characters/us/illidan/Sicilia"
    assert is_valid_raiderio_character(url) is True


def test_invalid_raiderio_url():
    url = "https://google.com"
    assert is_valid_raiderio_character(url) is False