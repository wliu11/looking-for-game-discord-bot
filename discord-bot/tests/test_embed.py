from utils.embed_builder import build_character_embed

def test_embed_builder():

    data = {
        "name": "Sicilia",
        "class": "Evoker",
        "realm": "Illidan",
        "region": "us"
    }

    embed = build_character_embed(data, 2500)

    assert embed.title == "Sicilia — Evoker"
    assert embed.fields[0].value == "Illidan"
    assert int(embed.fields[2].value) == 2500