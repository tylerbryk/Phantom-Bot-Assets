import os
os.system('pip install -U coc.py')
import coc
import time
import discord
import pandas as pd
from coc import utils
client = coc.login(os.getenv('EMAIL'), os.getenv('COCPWD'))


async def add_link(ctx, tag, raw_user):
	df = pd.read_csv('db.csv')
	if not df.loc[df['player_tag'] == tag].empty:
		for i in df['player_tag'].loc[df['player_tag'] == tag]: player_tag = i
		for i in df['discord_name'].loc[df['player_tag'] == tag]: name = i
		return await ctx.send(embed=discord.Embed(title='Already Linked!', description='{} is linked to {}'.format(player_tag, name)))
	try: user = await find_user(ctx, raw_user)
	except Exception: return await ctx.send(embed=discord.Embed(description="That user does not exist in this server!"))
	try: player_name, player_th, player_clan = await cocID_to_name(tag)
	except Exception: return await ctx.send(embed=discord.Embed(description='Invalid Player Tag!'))
	new = pd.DataFrame(data={'discord_id': [user.id], 'discord_name': ['{}#{}'.format(user.name, user.discriminator)], 'player_tag': [tag], 'player_name': [player_name], 'town_hall':[player_th], 'clan':[player_clan]})
	pd.concat([df, new], ignore_index=True).to_csv('db.csv', index=False)
	return await ctx.send(embed=discord.Embed(title='Linked!', description='{} linked to {}#{}'.format(tag, user.name, user.discriminator)))



async def get_link(ctx, arg):
	if '#' in arg:		# <---- If ARG is a player tag
		df = pd.read_csv('db.csv')
		if df.loc[df['player_tag'] == arg].empty:
			return await ctx.send(embed=discord.Embed(title='{} is not linked!'.format(arg), description='Please use %link <player_tag> <@discord_user> to link an account.'))
		for i in df['discord_id'].loc[df['player_tag'] == arg]: userID = i
		rows = df.loc[df['discord_id'] == userID]	
	elif '@' in arg: 	# <---- If ARG is a @discord user
		try: user = await find_user(ctx, arg)
		except Exception: return await ctx.send(embed=discord.Embed(description="That user does not exist in this server!"))
		df = pd.read_csv('db.csv')
		if df.loc[df['discord_id'] == user.id].empty:
			return await ctx.send(embed=discord.Embed(title='{} has no accounts!'.format(user.name), description='Please use %link <player_tag> <@discord_user> to link an account.'))
		rows = df.loc[df['discord_id'] == user.id]
	else: return await ctx.send(embed=discord.Embed(title='Invalid Input!', description='Please entire either a player tag or discord user.'))	
	account_list = ''
	for index, row in rows.iterrows():
		name = row['discord_name']
		account_list += '{} ({}) - TH{}\n'.format(row['player_name'], row['player_tag'], row['town_hall'])
	return await ctx.send(embed=discord.Embed(title='{}\'s Account(s)'.format(name), description=account_list))	


async def export_list(ctx):
	return await ctx.send(file=discord.File('db.csv', filename='linked_players.csv'))


async def update_db():
	df = pd.read_csv('db.csv')
	for index, row in df.iterrows():
		row['player_name'], row['town_hall'], row['clan'] = await cocID_to_name(row['player_tag'])
		df.loc[index] = row
		time.sleep(.1)
	df = df.sort_values(by=['discord_name', 'town_hall'])
	df.to_csv('db.csv', index=False)
	return



# =============== HELPERS ========================
async def find_user(ctx, raw_user):
	userID = raw_user.translate({ord(i): None for i in '<@>'})
	userID = userID.translate({ord(i): None for i in '!'})
	return ctx.guild.get_member(int(userID))

async def cocID_to_name(tag):
	if not utils.is_valid_tag(tag):
		return Exception
	player = await client.get_player(tag)
	return player.name, player.town_hall, str(player.clan)