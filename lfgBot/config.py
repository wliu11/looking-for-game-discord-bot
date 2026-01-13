
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Channel where welcome message will be sent
WELCOME_CHANNEL_ID = 1457894156025466880


# Role IDs
HEALER_ROLE_ID = 1459913185682522132
TANK_ROLE_ID = 1459913052370501682
DPS_ROLE_ID = 1459913257962836080

# Emoji → Role mapping
REACTION_ROLES = {
    "➕": HEALER_ROLE_ID,
    "🛡️": TANK_ROLE_ID,
    "⚔️": DPS_ROLE_ID,

}
