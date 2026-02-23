from urllib.parse import urlparse

def parse_raiderio_character_url(url: str):
    parsed = urlparse(url)
    parts = parsed.path.strip("/").split("/")

    # /characters/{region}/{realm}/{name}
    if len(parts) != 4 or parts[0] != "characters":
        raise ValueError("Invalid Raider.IO character URL")

    return {
        "region": parts[1],
        "realm": parts[2],
        "name": parts[3]
    }
