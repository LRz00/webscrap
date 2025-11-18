import discord
import asyncio
from src.configs.config import config

class DiscordNotifier:
    def __init__(self):
        intents = discord.Intents.default()
        self.token = config["discord_token"]
        self.channel_id = int(config["discord_server"])
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
        asyncio.run(self._run(message))

    async def _run(self, message: str):
        self.client.task = asyncio.create_task(self._send(message))
        await self.client.start(self.token)
