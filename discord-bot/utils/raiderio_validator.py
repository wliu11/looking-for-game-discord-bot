from urllib.parse import urlparse

VALID_REGIONS = {"us", "eu", "kr", "tw"}

def is_valid_raiderio_character(url: str) -> bool:
    """
    Validates Raider.IO character profile URLs.
    Example:
    https://raider.io/characters/us/illidan/Thrallslayer
    """
    try:
        parsed = urlparse(url)

        # Enforce HTTPS
        if parsed.scheme != "https":
            return False

        # Enforce domain
        if parsed.netloc not in {"raider.io", "www.raider.io"}:
            return False

        # Expected path:
        # /characters/{region}/{realm}/{character}
        parts = parsed.path.strip("/").split("/")

        if len(parts) != 4:
            return False

        if parts[0] != "characters":
            return False

        if parts[1] not in VALID_REGIONS:
            return False

        # realm + character must exist and not be empty
        if not parts[2] or not parts[3]:
            return False

        return True

    except Exception:
        return False
