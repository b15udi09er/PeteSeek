from discord import Forbidden
from .config import config

class ChannelGuard:
    @staticmethod
    async def verify(channel):
        """Check if bot can send messages"""
        try:
            await channel.send("🛡️ Permission check...", delete_after=0.1)
            return True
        except Forbidden:
            return False

    @staticmethod
    def is_allowed_channel(channel_id):
        return channel_id in config.response_channels