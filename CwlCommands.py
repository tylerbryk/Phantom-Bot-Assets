import os
import pymysql
import discord
import pandas as pd
from discord.ext import commands


class CwlCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='give')
    @commands.has_permissions(administrator=True)
    async def give_roles(self, ctx):
        msg = await ctx.send(embed=discord.Embed(title='Assigning CWL Roles!', color=0xf1c40f,
                                                 description='Hang tight, This operation may take several minutes.'))
        guild = self.client.get_guild(self.client.guild)
        db, cursor = await self.connect_db()
        roles = await self.build_roles(guild)
        cwl = pd.read_csv('cwl.csv')

        failed = []
        for clan, player_list in cwl.iteritems():
            for player in player_list:
                if pd.isna(player):
                    continue
                cursor.execute('SELECT discord_id FROM linked_accounts WHERE player_tag = "{}"'.format(player))
                result = cursor.fetchone()
                if not result:
                    failed.append(player)
                    continue
                try:
                    user = guild.get_member(result[0])
                    role = roles[clan]
                    await user.add_roles(role)
                except Exception:
                    failed.append(player)
                    continue
        if failed:
            players = [(await self.client.coc.get_player(tag)).name for tag in failed]
            failmsg = [tag + ' - ' + name for (tag, name) in zip(failed, players)]
            return await msg.edit(embed=discord.Embed(title='CWL Roles Assigned!', color=0x287e29,
                                                      description='Role assignment failed on:\n{}'
                                                      .format('\n'.join(failmsg))))
        return await msg.edit(embed=discord.Embed(title='CWL Roles Assigned!', color=0x287e29))

    @commands.command(name='remove-cwl')
    @commands.has_permissions(administrator=True)
    async def remove_cwl_roles(self, ctx):
        msg = await ctx.send(embed=discord.Embed(title='Removing CWL Roles!', color=0xf1c40f,
                                                 description='Hang tight, this operation may take a few minutes.'))
        guild = self.client.get_guild(self.client.guild)
        roles = (await self.build_roles(guild)).values()
        for role in roles:
            for member in role.members:
                await member.remove_roles(role)
        return await msg.edit(embed=discord.Embed(title='CWL Roles Removed!', color=0x287e29))

    @commands.command(name='remove-tourn')
    @commands.has_permissions(administrator=True)
    async def remove_tournament_roles(self, ctx):
        msg = await ctx.send(embed=discord.Embed(title='Removing Tournament Roles!', color=0xf1c40f,
                                                 description='Hang tight, this operation may take a few minutes.'))
        guild = self.client.get_guild(self.client.guild)
        roles = dict(
            TH14=guild.get_role(863856340949794827),
            TH13=guild.get_role(863856679066402816),
            TH12=guild.get_role(863857110600384512),
            TH11=guild.get_role(863857326813609994))
        for role in roles.values():
            for member in role.members:
                await member.remove_roles(role)
        return await msg.edit(embed=discord.Embed(title='Tournament Roles Removed!', color=0x287e29))

    @commands.command(name='cwlping')
    @commands.has_permissions(mention_everyone=True)
    async def ping_cwl_players(self, ctx, *fail):
        await ctx.send('Please move to the following clan:')
        guild = self.client.get_guild(self.client.guild)
        db, cursor = await self.connect_db()
        clans = await self.build_clans()
        cwl = pd.read_csv('cwl.csv')

        failed = []
        for clan, player_list in cwl.iteritems():
            move_players = {}
            for player in player_list:
                if pd.isna(player):
                    continue
                cursor.execute('SELECT * FROM linked_accounts WHERE player_tag = "{}"'.format(player))
                result = cursor.fetchone()
                if not result:
                    failed.append(player)
                    continue
                try:
                    user = guild.get_member(result[0])
                    if result[5] != clans[clan]:
                        move_players[result[3]] = user.mention  # {name : mention}
                except Exception:
                    failed.append(player)
                    continue
            msg = '\n'.join(['{} {}'.format(name, mention) for name, mention in move_players.items()])
            if msg:
                await ctx.send('**__{}__**\n{}'.format(clans[clan], msg))
        if fail and failed:
            players = [(await self.client.coc.get_player(tag)).name for tag in failed]
            msg = [tag + ' - ' + name for (tag, name) in zip(failed, players)]
            await ctx.send('**__Failed to ping:__**\n{}'.format('\n'.join(msg)))
        return

    @commands.command(name='stage')
    @commands.has_permissions(administrator=True)
    async def check_cwl_db(self, ctx):
        msg = await ctx.send(embed=discord.Embed(title='Staging...', description='ETA: 10 seconds', color=0xf1c40f))
        cwl = pd.read_csv('cwl.csv')
        db, cursor = await self.connect_db()
        failed = []
        for clan, player_list in cwl.iteritems():
            for player in player_list:
                if pd.isna(player):
                    continue
                cursor.execute('SELECT * FROM linked_accounts WHERE player_tag = "{}"'.format(player))
                if not cursor.fetchall():
                    failed.append(player)
        if failed:
            return await msg.edit(embed=discord.Embed(title='Missing Accounts:', color=0xf1c40f,
                                                      description='{}'.format('\n'.join(failed))))
        return await msg.edit(embed=discord.Embed(title='All Accounts Staged!', color=0x287e29))

    @staticmethod
    async def connect_db():
        db = pymysql.connect(
            host=os.getenv('HOST'),
            user=os.getenv('USER'),
            password=os.getenv('COCPWD'),
            database=os.getenv('USER'))
        return db, db.cursor()

    async def build_roles(self, guild):
        db, cursor = await self.connect_db()
        cursor.execute('SELECT abv, cwl_role_id FROM clans')
        result = cursor.fetchall()
        return {clan[0]: guild.get_role(clan[1]) for clan in result}

    async def build_clans(self):
        db, cursor = await self.connect_db()
        cursor.execute('SELECT abv, name FROM clans')
        result = cursor.fetchall()
        return {clan[0]: clan[1] for clan in result}


def setup(client):
    client.add_cog(CwlCommands(client))
