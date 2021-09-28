import discord
from discord.ext import commands


class ClanList(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='clear')
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx):
        return await ctx.channel.purge()

    @commands.command(name='clan-list')
    async def clan_list(self, ctx):
        await ctx.send(file=discord.File('Assets/clan_list.png'))
        clans = [
            ('#8Y8PQY8U', 'Main Clan'),
            ('#2RPL29QL', 'Feeder Clan - TH12+'),
            ('#RR89GL02', 'Feeder Clan - TH10+'),
            ('#8CCJ88PC', 'CWL Clan'),
            ('#9PRJR22U', 'CWL Clan'),
            ('#VG0LG9P2', 'CWL Clan'),
            ('#V80QJRU', 'CWL Clan'),
            ('#C98P9882', 'CWL Clan'),
            ('#G0VY0UL8', 'CWL Clan'),
            ('#29RRU898Y', 'ESL Clan'),
            ('#U0Y0VVR9', 'Chill Out Clan')
        ]

        for c in clans:
            clan = await self.client.coc.get_clan(c[0])
            e = discord.Embed(title=clan.name,
                              url=clan.share_link,
                              description=f'{c[1]}\n{clan.war_league.name}')
            e.set_thumbnail(url=clan.badge.url)
            await ctx.send(embed=e)


def setup(client):
    client.add_cog(ClanList(client))
