import os
import discord
import link as lk
from checkroles import checkroles
from flaskserver import start_server
from discord.ext import commands, tasks
client = commands.Bot(command_prefix='%', intents=discord.Intents.all())

# =============== GLOBAL VARIABLES ===================
guildID      = 819709187239313428
messageID    = 820481057525727273
dz_channel   = 819709187822583813
gc_channel   = 819709187822583814
sc_channel   = 819709187822583816
welc_channel = 819709187822583812
roleID_dzRc  = '<@&819709187285975073>'
roleID_gcRc  = '<@&819709187285975072>'
roleID_scRc  = '<@&819709187285975071>'
roleID_gaRc  = '<@&819709187285975070>'
server_rules = '<#819709187613392913>'
dz_rules     = '<#819709187613392914>'
gc_rules     = '<#819709187613392915>'
sc_rules     = '<#819709187822583808>'
dz_emoji     = 820093624002805771
gc_emoji     = 820093624456183808
sc_emoji     = 820093624434950154
ga_emoji     = 820103306604707860
# =====================================================

@client.event
async def on_ready():
	print('Bot Online!')
	update_db_loop.start()
	await client.change_presence(activity=discord.Game('Clash of Clans'))


@client.event
async def on_raw_reaction_add(ctx):
	if ctx.message_id != messageID:
		return
	message = "{} is applying for **{}**\n\nPlease do the following:\n1. Read the {} and {}\n2. Send a screenshot of your base\n3. Send a screenshot of your profile\n4. Send your player tag (Ex: #5GC47AE)\n\nA{} {} will be online to assist you shortly!\n\n"
	if ctx.emoji.id == dz_emoji:
		channel = client.get_channel(dz_channel)
		await channel.send(message.format(ctx.member.mention, 
																			'Danger Zone', server_rules, dz_rules, '', roleID_dzRc))
	elif ctx.emoji.id == gc_emoji:
		channel = client.get_channel(gc_channel)
		await channel.send(message.format(ctx.member.mention, 
																			'Game Changers', server_rules, gc_rules, 'n', roleID_gcRc))
	elif ctx.emoji.id == sc_emoji:
		channel = client.get_channel(sc_channel)
		await channel.send(message.format(ctx.member.mention, 
																			'Stormcloaks', server_rules, sc_rules, '', roleID_scRc))
	elif ctx.emoji.id == ga_emoji:
		channel = client.get_channel(welc_channel)
		await channel.send('{} is a **General Applicant**\n\nPlease do the following:\n1. Read the {}\n2. Send a screenshot of your base\n3. Send a screenshot of your profile\n4. Send your player tag (Ex: #5GC47AE)\n\nA {} will be online to assist you shortly!'.format(ctx.member.mention, server_rules, roleID_gaRc))
	else:
		channel = client.get_channel(welc_channel)
		await channel.send('{} reacted with an invalid option!\nPlease visit {} and select a clan application type!'.format(ctx.member.mention, server_rules))


@client.command()
async def check(ctx, role):
	await checkroles(ctx, role)

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
	await lk.update_db()

#@client.command()
#async def delete(ctx):
  #await ctx.channel.purge()


# =============== BACKGROUND TASKS ===================
@tasks.loop(minutes=2) 
async def update_db_loop():
	await lk.update_db()

#@tasks.loop(minutes=1) 
#async def check_for_inactives():
	#guild = client.get_guild(guildID)
	#for member in guild.members:
		#if len(member.roles) <= 1 and fc.time_passed(member, 3):
			# TODO: Implement no-role notifier here...

start_server()
client.run(os.getenv('TOKEN'))