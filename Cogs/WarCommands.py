import os
import time
from datetime import datetime

import pymysql
import discord
from discord.ext import commands


class WarCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='war')
    async def war_ping(self, ctx, abv):
        db, cursor = await self.connect_db()
        cursor.execute('SELECT * FROM clans WHERE abv = "{}"'.format(abv))
        result = cursor.fetchall()
        if not result:
            return await ctx.send(
                'Invalid input! Please enter the two-letter abbreviation for the desired clan. (DZ, GC, etc.)')
        tag = result[0][2]
        war = await self.client.coc.get_current_war(tag)
        guild = self.client.get_guild(self.client.emoji_guild)
        em = {name: (await guild.fetch_emoji(id)) for name, id in self.client.emoji_dict.items()}
        gmt = datetime.fromtimestamp(time.mktime(time.gmtime()))
        d = '**War Against**\n{} ({})\n\n'.format(war.opponent.name, war.opponent.tag)
        if war.state == 'preparation':
            t = time.gmtime((war.start_time.time - gmt).total_seconds())
            d += '**War State**\nPreparation ({} vs {})\nStarts in {}\n\n'.format(war.team_size, war.team_size,
                                                                                  time.strftime('%Hh %Mm', t))
        elif war.state == 'inWar':
            t = time.gmtime((war.end_time.time - gmt).total_seconds())
            d += '**War State**\nBattle Day ({} vs {})\nEnds in {}\n\n'.format(war.team_size, war.team_size,
                                                                               time.strftime('%Hh %Mm', t))
        elif war.state == 'warEnded':
            t = time.gmtime((gmt - war.end_time.time).total_seconds())
            d += '**War State**\nWar Ended ({} vs {})\nEnded {} ago\n\n'.format(war.team_size, war.team_size,
                                                                                time.strftime('%Hh %Mm', t))
        else:
            clan = await self.client.coc.get_clan(tag)
            return await ctx.send('{} does not have any recent war activity!'.format(clan.name))
        if war.state == 'inWar' or war.state == 'warEnded':
            attacks = await self.get_attack_info(war)
            size = war.team_size
            if not war.is_cwl:
                size *= 2
            d += '**Stats**\n{}\t{}\t{}\n'.format(attacks['h_star'], em['STAR'], attacks['e_star'])
            d += '{}%\t{}\t{}%\n'.format(attacks['h_dest'], em['FIRE'], attacks['e_dest'])
            d += '{}/{}\t{}\t{}/{}\n\n'.format(attacks['h_hits'], size, em['SWRD'], attacks['e_hits'], size)
        home, away = await self.get_th_composition(war)
        d += '**Composition**\n{}\n'.format(war.clan.name)
        for th, amt in home.items():
            d += '\t' + '{} {}'.format(em[th], amt)
        d += '\n\n{}\n'.format(war.opponent.name)
        for th, amt in away.items():
            d += '\t' + '{} {}'.format(em[th], amt)
        ping_only = None
        if war.state == 'inWar':
            home_attacks = await self.get_home_attacks(war, tag)
            player_tags = await self.get_home_players(war, tag)
            remain_hits = await self.attacks_remaining(home_attacks, player_tags, cwl=war.is_cwl)
            full_ping, ping_only = await self.tag_to_name(remain_hits)
            if full_ping:
                d += '\n\n**Remaining Attacks**\n{}'.format('\n'.join(full_ping))
        e = discord.Embed(description=d, color=0x3498db)
        e.set_author(name='{} ({})'.format(war.clan.name, war.clan.tag), icon_url=war.clan.badge.small)
        await ctx.send(embed=e)
        if ping_only:
            await ctx.send(' '.join(ping_only))
        return

    @staticmethod
    async def get_th_composition(war):
        home, away = {}, {}
        for member in war.members:
            if member.clan.name == war.clan.name:
                if 'TH' + str(member.town_hall) not in home:
                    home['TH' + str(member.town_hall)] = 1
                else:
                    home['TH' + str(member.town_hall)] += 1
            else:
                if 'TH' + str(member.town_hall) not in away:
                    away['TH' + str(member.town_hall)] = 1
                else:
                    away['TH' + str(member.town_hall)] += 1
        return home, away

    @staticmethod
    async def get_attack_info(war):
        info = dict(
            h_star=0, e_star=0,
            h_dest=0, e_dest=0,
            h_hits=0, e_hits=0)
        attacks = dict()
        for attack in war.attacks:
            if attack.defender_tag not in attacks:
                attacks[attack.defender_tag] = [attack.stars, attack.destruction, attack.attacker]
            else:
                star = attacks[attack.defender_tag][0]
                dest = attacks[attack.defender_tag][1]
                if star < attack.stars:
                    attacks[attack.defender_tag][0] = attack.stars
                if dest < attack.destruction:
                    attacks[attack.defender_tag][1] = attack.destruction
            if attack.attacker.is_opponent:
                info['e_hits'] += 1
            else:
                info['h_hits'] += 1
        for tag, items in attacks.items():
            if items[2].is_opponent:
                info['e_star'] += items[0]
                info['e_dest'] += items[1]
            else:
                info['h_star'] += items[0]
                info['h_dest'] += items[1]
        info['h_dest'] = round((info['h_dest'] / war.team_size), 2)
        info['e_dest'] = round((info['e_dest'] / war.team_size), 2)
        return info

    @staticmethod
    async def get_home_attacks(war, tag):
        home_attack_tags = {}
        for attack in war.attacks:
            if attack.attacker.clan.tag == tag:
                player_tag = attack.attacker.tag
                if player_tag in home_attack_tags:
                    home_attack_tags[player_tag] += 1
                else:
                    home_attack_tags[player_tag] = 1
        return home_attack_tags

    @staticmethod
    async def get_home_players(war, tag):
        home_players = []
        for member in war.members:
            if member.clan.tag == tag:
                home_players.append(member.tag)
        return home_players

    @staticmethod
    async def attacks_remaining(home_attacks, player_tags, cwl):
        remaining = []
        for tag in player_tags:
            if tag not in home_attacks:
                remaining.append(tag)
            else:
                if cwl is False and home_attacks[tag] == 1:
                    remaining.append(tag)
        return remaining

    @staticmethod
    async def connect_db():
        db = pymysql.connect(
            host=os.getenv('HOST'),
            user=os.getenv('USER'),
            password=os.getenv('COCPWD'),
            database=os.getenv('USER'))
        return db, db.cursor()

    async def tag_to_name(self, tags):
        db, cursor = await self.connect_db()
        guild = self.client.get_guild(self.client.guild)
        full, ping = [], []
        for tag in tags:
            cursor.execute('SELECT * FROM linked_accounts WHERE player_tag = "{}"'.format(tag))
            result = cursor.fetchall()
            if result is None:
                player = await self.client.coc.get_player(tag)
                full.append(player.name)
                continue
            user = guild.get_member(result[0][0])
            full.append('{} - {}'.format(result[0][3], user.mention))
            ping.append(user.mention)
        return full, ping


def setup(client):
    client.add_cog(WarCommands(client))
