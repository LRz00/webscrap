import discord
import asyncio
from src.configs.config import config

class DiscordNotifier:
    def __init__(self):
        intents = discord.Intents.default()
        self.token = config.get("discord_token", "")
        discord_server = config.get("discord_server", "")
        
        if not self.token:
            raise ValueError("discord_token is required in config")
        if not discord_server:
            raise ValueError("discord_server is required in config")
        
        try:
            self.channel_id = int(discord_server)
        except ValueError:
            raise ValueError(f"discord_server must be a valid integer, got: {discord_server}")
        
        self.client = discord.Client(intents=intents)

    async def _send(self, message: str):
        await self.client.wait_until_ready()
        channel = self.client.get_channel(self.channel_id)

        if channel is None:
            print("Erro: canal não encontrado no Discord")
        else:
            await channel.send(message)

        await self.client.close() 

    def send_message(self, message: str):
        try:
            asyncio.run(self._run(message))
        except Exception as e:
            print(f"Error sending Discord message: {e}")
            raise

    async def _run(self, message: str):
        self.client.task = asyncio.create_task(self._send(message))
        await self.client.start(self.token)
