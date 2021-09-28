import os
import coc
# import Server
import discord
from discord.ext import commands

extensions = ['ClanList']


class RoyalBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='%%', intents=discord.Intents.all())
        self.coc = coc.login(os.getenv('EMAIL'), os.getenv('COCPWD'), client=coc.Client)
        for ext in extensions:
            self.load_extension(ext)

    async def on_ready(self):
        print('Bot Online!')
        await self.change_presence(activity=discord.Game('Clash of Clans'))

    def run_bot(self):
        # Server.start()
        super().run(os.getenv('TOKEN'))


if __name__ == '__main__':
    RoyalBot().run_bot()
