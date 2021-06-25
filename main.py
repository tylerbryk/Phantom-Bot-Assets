import os
import cwl
import redd
import flasks
import discord
import applicant
import link as lk
import checkroles as cr
from datetime import datetime
from discord.ext import commands, tasks
client = commands.Bot(command_prefix='%', intents=discord.Intents.all())

@client.event
async def on_ready():
	print('Bot Online!')
	reddit_reminder.start()
	await client.change_presence(activity=discord.Game('Clash of Clans'))

@client.event
async def on_raw_reaction_add(ctx):
	await applicant.applicant_ping(ctx, client)

@client.listen()
async def on_message(ctx):
	await redd.check_subred(ctx, client)

@client.command()
async def check(ctx, role):
	await cr.checkroles(ctx, role)

@client.command()
async def link(ctx, tag, user):
	await lk.add_link(ctx, tag, user)

@client.command()
async def get(ctx, arg):
	await lk.get_link(ctx, arg)

@client.command()
async def export(ctx):
	await lk.export_list(ctx)

@client.command()
async def update(ctx):
	await lk.update_db(ctx)

@client.command()
async def len(ctx):
	await lk.db_len(ctx)

# ===== CLEAN DB =====
@client.command()
async def clean(ctx):
	await lk.clean_db(ctx, client)

# ===== CWL COMMANDS =====
@client.command()
async def cwldisp(ctx):
	await cwl.display_missing_players(ctx, client)

@client.command()
async def cwlping(ctx):
	await cwl.ping_missing_players(ctx, client)

# ===== WAR PING =====
@client.command()
async def war(ctx, clan='all'):
	await cwl.war_ping(ctx, clan, client)

@client.command()
async def score(ctx, clan='all'):
	await cwl.score_clan(ctx, clan)

#@client.command()
#async def give(ctx):
#	await cwl.give_roles(ctx, client)

@client.command()
async def remind(ctx):
	await redd.reminder(client)


# =============== BACKGROUND TASKS ===================
@tasks.loop(minutes=1)
async def reddit_reminder():
	if datetime.now().hour == 17 and datetime.now().minute == 0:
		return await redd.reminder(client)
# =====================================================


flasks.start_server()
client.run(os.getenv('TOKEN'))