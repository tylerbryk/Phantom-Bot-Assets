import discord
from discord.ext import commands


server_rules_text = '''1)** __Nickname__**
> • Your Discord nickname must represent your clash of clans account name(s)

2)** __No Toxicity__**
> • This includes and is not limited to, homophobia, racism, sexism, and intentionally being harmful to others

3)** __No BST__**
> • No buying, selling, or trading of accounts

4)** __No Drama__**
> • No starting or escalating drama
> • If you have a problem, deal with it privately
> • If you need help dealing with anything related to this, bring it to leadership

5) **__No Political Conversations__**
> • Everyone is entitled to their political opinions, but clash of clans is not the place to talk about them

6)** __CWL__**
> • Participants must register via the form sent at the end of each month
> • Players must be understanding that they may be relocated for CWL
> • This allows players to be in the best league based on their skill level
> • Heroes must be up for CWL, no exceptions
> • Participants will vote on who earns bonuses for each clan


<:DZ:852634339844816966> **DANGER ZONE**
> • Main clan in the Phantom family
> • TH14 only
> • Currently ranked Champion League I
> • Competitive and helpful environment
> • Read <#819709187613392914> for more info
> • FC’s will be required upon entry for new applicants

<:DL:858033764453580820> **DOWNFALL LEGEND**
> • TH13+ (TH14 or near max TH13)
> • Currently ranked Champion League II
> • Competitive and helpful environment
> • Read <#819709187822583808> for more info
> • FC’s will be required upon entry for new applicants

<:GC:852634339954917466> **GAME CHANGERS**
> • TH12+ only
> • Currently ranked Masters I
> • Calm and friendly environment
> • Read <#819709187613392915> for more info
> • FC’s will be required upon entry for new applicants

⬆️ **SCROLL UP!** ⬆️
'''

# =============================================================================================================

dz_rules_text = '''**__Requirements:__**
> • TH14 Only
> • BK80, AQ80, GW55, RC30
> • Max or near max bases only

**__Clan Games:__**
> • Not mandatory 
> • 1000 pt. minimum if you do participate 

**__Donations:__** 
> • No donation ratio or requirements
> • Donate as much as possible
> • Make an effort to fill pending donation requests before requesting yourself
> • Having little or no donations at the end of the season may result in a kick

**__War Rules:__**
> • All heroes must be up for war 
> • No hits in the first hour
> • First hour is used to scout and claim bases of the **same** town hall
> • Claim the highest ranked base that you are confident in tripling
> • If a claimed base has not been hit after the first 12 hours, it is fair game
> • Feel free to cleanup/triple a base after the 12-hour mark
> • Both attacks are **mandatory** and should be done by the 23-hour mark

**__CWL Rules:__**
> • Register via the form sent at the end of each month
> • All heroes must be up during CWL week
> • CWL lineups will be sent out before the 1st day of each month 
> • You may be assigned to this clan, or a similarly ranked clan in the family
> • Clan selection is based on war hits, war defenses, and friendly challenges 
> • Before attacking in CWL, you are **required** to submit a plan on Discord
> • No attacking in the first hour as this time should be used to claim a base
> • Feel free to reach out to leadership should you ever need anything

**__Attack Planning Resources:__**
> • Spotter on Voice Chat
> • Collaborating with other team members
> • Using our clash / Burnt Base bots

⬆️ **SCROLL UP!** ⬆️
'''

# =============================================================================================================

dl_rules_text = '''**__Requirements:__**
> • TH13 BK70, AQ70, GW45, RC15
> • TH14 BK75, AQ75, GW50, RC25
> • Base at least 90% max from previous Town Hall

**__Clan Games:__**
> • 1000 point minimum

**__Donations:__**
> • No donation ratio or requirements
> • Donate as much as possible
> • Make an effort to fill pending donation requests before requesting yourself
> • Having little or no donations at the end of the season may result in a kick

**__War Rules:__**
> • All heroes must be up for war
> • No hits in the first hour
> • First hour is used to scout and claim bases of the **same** town hall
> • Claim the highest ranked base that you are confident in tripling
> • If a claimed base has not been hit after the first 12 hours, it is fair game
> • Feel free to cleanup/triple a base after the 12-hour mark
> • Both attacks are **mandatory** and should be done by the 23-hour mark

**__CWL Rules:__**
> • Register via the form sent at the end of each month
> • All heroes must be up during CWL week
> • CWL lineups will be sent out before the 1st day of each month
> • You may be assigned to this clan, or a similarly ranked clan in the family
> • Clan selection is based on war hits, war defenses, and friendly challenges
> • Before attacking in CWL, you are **required** to submit a plan on Discord
> • No attacking in the first hour as this time should be used to claim a base
> • Feel free to reach out to leadership should you ever need anything

**__Attack Planning Resources:__**
> • Spotter on Voice Chat
> • Collaborating with other team members
> • Using our clash / Burnt Base bots

⬆️ **SCROLL UP!** ⬆️
'''

# =============================================================================================================

roles_text = '''**Management:**
> <@&819709187323199511>
> <@&819709187323199510>
> <@&819709187315466268>

**Leadership:**
> <@&819709187315466264>
> <@&819709187315466267>
> <@&819709187315466265>

**Legendary Roles:**
> <@&819709187315466263>
> <@&819709187315466261>
> <@&819709187315466262>

**Main Clans:**
> <@&819709187302359059>
> <@&858006003042746399>

**Ranks:**
> <@&819709187302359053>
> <@&819709187302359052>

**Helper Roles:**
> <@&819709187268411410>
> <@&819709187302359050>
> <@&819709187302359051>

**Family Friends:**
> <@&819709187285975079>
> <@&820169532207005696>
> <@&820171267146514432>

**Recruiter Roles:**
> <@&819709187285975070>
> <@&819709187285975073>
> <@&819709187285975071>

**CWL Clan Roles:**
> <@&819709187268411409>
> <@&858032092519596042>
> <@&819793045318139905>
> <@&819709187268411408>
> <@&819793325125009438>
> <@&819793579495915531>
> <@&819709187268411406>
> <@&819709187268411405>
> <@&825947360538132500>
> <@&837775900463726662>
> <@&849075141560631307>

**Townhall Roles:**
> <@&833162119477723136>
> <@&819709187239313436>
> <@&819709187239313435>
> <@&819709187239313434>
> <@&819709187239313433>

**Applicant Roles:**
> <@&819709187285975075>
> <@&819709187285975078>
> <@&819709187285975076>
'''

# =============================================================================================================

horde_text = '''Phantom Family's competitive squad for tournaments, leagues, and events!

The team comprises of only max TH13’s from the family who are seeking a more competitive way of playing the game. 

The team has competed in Warriors Champions League (WCL), Blitzkreig, Clash Masters League (CML), and Universal War league (UWL), to name a few.

If you are interested in joining, want more information, or just want to check out the server, then click the link below! 
https://discord.gg/d3E8wkM'''


class InfoCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='info-rules')
    @commands.has_permissions(administrator=True)
    async def send_server_rules(self, ctx):
        await ctx.send(file=discord.File('banners/server_rules.png'))
        await ctx.send(server_rules_text)

    @commands.command(name='info-dz-rules')
    @commands.has_permissions(administrator=True)
    async def send_dz_rules(self, ctx):
        await ctx.send(file=discord.File('banners/dz_rules.png'))
        await ctx.send(dz_rules_text)

    @commands.command(name='info-dl-rules')
    @commands.has_permissions(administrator=True)
    async def send_dl_rules(self, ctx):
        await ctx.send(file=discord.File('banners/dl_rules.png'))
        await ctx.send(dl_rules_text)

    @commands.command(name='info-roles')
    @commands.has_permissions(administrator=True)
    async def send_role_info(self, ctx):
        await ctx.send(file=discord.File('banners/role_info.png'))
        await ctx.send(roles_text)


def setup(client):
    client.add_cog(InfoCommands(client))
