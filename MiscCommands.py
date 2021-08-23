import os
import pymysql
import discord
from datetime import datetime
from discord.ext import commands, tasks

# === Applicant Variables ===
message_id = 858441901416775700
dz_channel = 819709187822583813
dl_channel = 819709187822583816
gc_channel = 819709187822583814
wlc_channel = 819709187822583812
dz_role = '<@&819709187285975073>'
dl_role = '<@&819709187285975071>'
gc_role = '<@&819709187285975072>'
rc_role = '<@&819709187285975070>'
sr_rules = '<#819709187613392913>'
dz_rules = '<#819709187613392914>'
dl_rules = '<#819709187822583808>'
gc_rules = '<#819709187613392915>'
dz_emoji = 852634339844816966
dl_emoji = 858033764453580820
gc_emoji = 852634339954917466
ga_emoji = 820103306604707860

# === Recruitment Variables ===
nr_red_ch_id = 675444353237516314
ph_red_ch_id = 819709189181800481
reminder_ch_id = 819709189181800480


class MiscCommands(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.reddit_reminder.start()

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, ctx):
        await self.applicant_ping(ctx)

    @commands.Cog.listener()
    async def on_message(self, ctx):
        await self.forward_reddit(ctx)

    @commands.command(name='clear')
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx):
        return await ctx.channel.purge()

    @commands.command(name='clan-list')
    async def clan_list(self, ctx):
        await ctx.send(file=discord.File('banners/clan_list.png'))
        db, cursor = await self.connect_db()
        cursor.execute('SELECT tag, description FROM clans')
        results = cursor.fetchall()
        for r in results:
            clan = await self.client.coc.get_clan(r[0])
            e = discord.Embed(title=clan.name,
                              url=clan.share_link,
                              description=f'{r[1]}\n{clan.war_league.name}')
            e.set_thumbnail(url=clan.badge.url)
            await ctx.send(embed=e)

    async def applicant_ping(self, ctx):
        if ctx.message_id != message_id:
            return

        message = '{} is applying for **{}**\n\nPlease do the following:\n1. Read {} and {}\n2. Send a screenshot of your base and profile\n3. Send your player tag (Ex: #5GC47AE)\n\nA {} will be online to assist you shortly!'

        if ctx.emoji.id == dz_emoji:
            channel = self.client.get_channel(dz_channel)
            await channel.send(message.format(ctx.member.mention,
                                              'Danger Zone', sr_rules, dz_rules, dz_role))
        elif ctx.emoji.id == dl_emoji:
            channel = self.client.get_channel(dl_channel)
            await channel.send(message.format(ctx.member.mention,
                                              'Downfall Legend', sr_rules, dl_rules, dl_role))
        elif ctx.emoji.id == gc_emoji:
            channel = self.client.get_channel(gc_channel)
            await channel.send(message.format(ctx.member.mention,
                                              'Game Changers', sr_rules, gc_rules, gc_role))
        elif ctx.emoji.id == ga_emoji:
            channel = self.client.get_channel(wlc_channel)
            await channel.send('{} is a **General Applicant**\n\nPlease do the following:\n1. Read {}\n2. Send a screenshot of your base and profile\n3. Send your player tag (Ex: #5GC47AE)\n\nA {} will be online to assist you shortly!'.format(ctx.member.mention, sr_rules, rc_role))
        else:
            channel = self.client.get_channel(wlc_channel)
            await channel.send(
                '{} reacted with an invalid option!\nPlease visit {} and select a clan application type!'.format(
                    ctx.member.mention, sr_rules))

    async def forward_reddit(self, ctx):
        if ctx.channel.id != nr_red_ch_id or not ctx.embeds:
            return
        channel = self.client.get_channel(ph_red_ch_id)
        for embed in ctx.embeds:
            await channel.send(embed=embed)
        return

    @tasks.loop(minutes=1)
    async def reddit_reminder(self):
        if datetime.now().hour == 19 and datetime.now().minute == 0:  # 3pm
            day = datetime.today().weekday()
            db, cursor = await self.connect_db()
            cursor.execute('SELECT * FROM recruitment_reminders WHERE day = "{}"'.format(day))
            result = cursor.fetchall()
            channel = self.client.get_channel(reminder_ch_id)
            if not result:
                return await channel.send('**No Recruitment Reminders Today**')
            rc = self.client.get_user(result[0][3])
            return await channel.send('**Recruitment Post Reminder**\nPlease post for {} {}'.format(result[0][1], rc.mention))

    @staticmethod
    async def connect_db():
        db = pymysql.connect(
            host=os.getenv('HOST'),
            user=os.getenv('USER'),
            password=os.getenv('COCPWD'),
            database=os.getenv('USER'))
        return db, db.cursor()


def setup(client):
    client.add_cog(MiscCommands(client))
