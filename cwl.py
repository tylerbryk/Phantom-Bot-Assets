# ==============================
guild_id = 819709187239313428
# ==============================
from datetime import datetime
import os
import pandas as pd
import discord
import time
os.system('pip install -U coc.py')
import coc
coc_client = coc.login(os.getenv('EMAIL'), os.getenv('COCPWD'), client=coc.Client, key_names='Phantom Bot', key_count=1)

def get_clans():
	clans = dict(
		DZ = 'DANGER ZONE',
		NR = 'Night Raiderz',
		DL = 'Downfall Legend',
		GC = '*G@ME CHANGERS*',
		AL = 'Anstaloopeezi',
		SC = 'Stormcloaks',
		BH = 'Beasthole Utd®',
		SM = 'the spoonmaster',
		CW = 'CIKALAN WAR',
		ML = 'Miniloopeezi', 
		GS = '★Gear Savana★',
		SW = 'Soul Wreckers')
	return clans

def get_tags():
	tags = dict(
		DZ = '#CP90GG2Q',
		NR = '#8P8GPYPJ',
		DL = '#8LPGJQ0R',
		GC = '#LP8RL9L0',
		AL = '#22Y9CL89R',
		SC = '#80RQQUVJ',
		BH = '#2Y0G20G',
		SM = '#Y92RLQUY',
		CW = '#UYQUGG0P',
		ML = '#28QRLUUP0',
		GS = '#JQQGPCQ0',
		SW = '#Y2Y8RQ2L')
	return tags

def get_roles(guild):
	roles = dict(
	DZ = guild.get_role(819709187268411409),
	DL = guild.get_role(858032092519596042),
	NR = guild.get_role(819793045318139905),
	GC = guild.get_role(819709187268411408),
	AL = guild.get_role(819793579495915531),
	SC = guild.get_role(819793325125009438),
	BH = guild.get_role(819709187268411406),
	SM = guild.get_role(819709187268411407),
	CW = guild.get_role(819709187268411405),
	ML = guild.get_role(825947360538132500),
	GS = guild.get_role(837775900463726662),
	SW = guild.get_role(849075141560631307),
	TH14 = guild.get_role(863856340949794827),
	TH13 = guild.get_role(863856679066402816),
	TH12 = guild.get_role(863857110600384512),
	TH11 = guild.get_role(863857326813609994))
	return roles


async def ping_missing_players(ctx, client):
	guild = client.get_guild(guild_id)
	cwl = pd.read_csv('cwl.csv')
	db  = pd.read_csv('db.csv')
	clans = get_clans()

	move_players = {}
	failed_players = []
	for clan, player_list in cwl.iteritems():
		for player in player_list:
			if pd.isna(player):
				continue
			try: 
				cur_clan = db.loc[db['player_name'] == player]['clan'].item()
			except ValueError:
				print('Failed to locate {} in the database!'.format(player))
				failed_players.append(player)
				continue
			try: 
				id = db.loc[db['player_name'] == player]['discord_id'].item()
			except ValueError:
				print('Failed to locate {} in the database!'.format(player))
				failed_players.append(player)
				continue
			try: user = guild.get_member(id)
			except Exception: 
				print('Error retrieving {} profile from ID!'.format(player))
				failed_players.append(player)
				continue
			if cur_clan != clans[clan]:
				move_players[player] = [clan, user.mention]
	print_str = []
	for key, val in move_players.items():
		print_str.append('{}: {} {}'.format(val[0], key, val[1]))
	await ctx.send('The following accounts still need to move to the appropriate CWL clan:\n\n{}'.format('\n'.join(print_str)))
	return


async def display_missing_players(ctx, client):
	cwl = pd.read_csv('cwl.csv')
	db  = pd.read_csv('db.csv')
	clans = get_clans()
	move_players = {}
	for clan, player_list in cwl.iteritems():
		for player in player_list:
			if pd.isna(player):
				continue
			try: 
				cur_clan = db.loc[db['player_name'] == player]['clan'].item()
			except ValueError:
				print('Failed to locate {} in the database!'.format(player))
			if cur_clan != clans[clan]:
				move_players[player] = clan
	print_str = []
	for key, val in move_players.items():
		print_str.append('{}: {}'.format(val, key))
	await ctx.send(embed=discord.Embed(title='Move these accounts!', description='The following accounts still need to move to the appropriate CWL clan:\n\n{}'.format('\n'.join(print_str))))
	return


async def give_roles(ctx, client):
	await ctx.send(embed=discord.Embed(title='Assigning CWL Roles!', description='This operation may take several minutes. A confirmation message will be displayed when complete.'))

	guild = client.get_guild(guild_id)
	try: roles = get_roles(guild)
	except Exception: await ctx.send('Error getting roles from ID!')

	cwl = pd.read_csv('cwl.csv')
	db  = pd.read_csv('db.csv')

	accs_linked = 0
	failed_players = []
	for clan, player_list in cwl.iteritems():
		for player in player_list:
			if pd.isna(player):
				continue
			try: 
				id = db.loc[db['player_name'] == player]['discord_id'].item()
			except ValueError:
				print('Failed to locate {} in the database!'.format(player))
				failed_players.append(player)
			try: user = guild.get_member(id)
			except Exception: 
				print('Error retrieving {} profile from ID!'.format(player))
				failed_players.append(player)
			try: role = roles[clan]
			except KeyError: print('Clan name {} doesn\'t exist in DB!'.format(clan))
			try: await user.add_roles(role)
			except Exception: 
				print('Failed to give {} roles!'.format(player))
				failed_players.append(player)
			accs_linked += 1
	await ctx.send(embed=discord.Embed(title='CWL roles assigned to {} players!'.format(accs_linked), description='Failed to assign roles to the following players:\n{}'.format('\n'.join(failed_players))))
	return


async def check_cwldb(ctx):
	cwl = pd.read_csv('cwl.csv')
	db  = pd.read_csv('db.csv')
	in_db = []
	failed_players = []
	for clan, player_list in cwl.iteritems():
		for player in player_list:
			if pd.isna(player):
				continue
			try: 
				in_db.append(db.loc[db['player_name'] == player]['discord_id'].item())
			except:
				print('Failed to locate {} in the database!'.format(player))
				failed_players.append(player)
	return


# ============================================================



async def war_ping(ctx, clan, client):
	if clan == 'all':
		await war_ping_all(ctx, client)
		return
	clan_tags = get_tags()
	clans = get_clans()
	try: clan_tag = clan_tags[clan]
	except Exception:
		await ctx.send(embed=discord.Embed(title='Incorrect Clan!', 
		description='Please enter the capital two-letter abbreviation for the desired clan. (DZ, GC, etc.)'))
		return
	try: war = await coc_client.get_current_war(clan_tag)
	except Exception:
		await ctx.send('An error occured while trying to fetch the latest war information from CoC API!')
		return
	if war.state == 'notInWar':
		await ctx.send('{} is not currently in war!'.format(clans[clan]))
		return
	attack_tags = await get_home_attacks(war, clan_tag)
	player_tags = await get_home_players(war, clan_tag)
	remain_hits = await attacks_remaining(attack_tags, player_tags, cwl=war.is_cwl)
	ping = await playertag_to_name(remain_hits, client)
	t = war.end_time.time - datetime.now()
	t_rem = time.gmtime(t.total_seconds())
	if not ping:
		await ctx.send('**All Attacks Completed!**\n\nWar ending in {}'.format(time.strftime('%H hours %M minutes', t_rem)))
		return
	await ctx.send('**War Hit Reminder!** - {}\n\n{}\n\n**War ending in {}!**'.format(clans[clan], '\n'.join(ping), time.strftime('%H hours %M minutes', t_rem)))
	return 


async def war_ping_all(ctx, client):
	clan_tags = get_tags()
	clans = get_clans()
	for clan in clans.keys():
		clan_tag = clan_tags[clan]
		try: war = await coc_client.get_current_war(clan_tag)
		except Exception:
			print('An error occured while trying to fetch the latest war information from CoC API!')
			continue
		if war.state == 'notInWar':
			continue
		attack_tags = await get_home_attacks(war, clan_tag)
		player_tags = await get_home_players(war, clan_tag)
		remain_hits = await attacks_remaining(attack_tags, player_tags, cwl=war.is_cwl)
		ping = await playertag_to_name(remain_hits, client)
		if not ping:
			continue
		e = discord.Embed(title='{} - Missing Attacks'.format(clans[clan]), description='\n'.join(ping))
		await ctx.send(embed=e)
	return 


async def get_home_attacks(war, clantag):
	home_attack_tags = {}
	for attack in war.attacks:
		if attack.attacker.clan.tag == clantag:
			player_tag = attack.attacker.tag
			if player_tag in home_attack_tags:
				home_attack_tags[player_tag] += 1
			else:
				home_attack_tags[player_tag] = 1
	return home_attack_tags


async def get_home_players(war, clantag):
	home_players = []
	for member in war.members:
		if member.clan.tag == clantag:
			home_players.append(member.tag)
	return home_players


async def attacks_remaining(attack_tags, player_tags, cwl):
	remaining = []
	for tag in player_tags:
		if tag not in attack_tags:
			remaining.append(tag)
		else:
			if cwl == False and attack_tags[tag] == 1:
				remaining.append(tag)
	return remaining


async def playertag_to_name(tags, client):
	guild = client.get_guild(guild_id)
	db = pd.read_csv('db.csv')
	ping = []
	for tag in tags:
		row = db.loc[db['player_tag'] == tag]
		try: id = row['discord_id'].item()
		except ValueError:
			player = await coc_client.get_player(tag)
			ping.append(player.name)
			continue
		name = row['player_name'].item()
		try: user = guild.get_member(id)
		except Exception: print('Error retrieving {} profile from ID!'.format(name))
		ping.append('{} {}'.format(name, user.mention))
	return ping



# ==============================================================



async def score_clan(ctx, clan):
	if clan == 'all':
		await score_all(ctx)
		return
	clan_tags = get_tags()
	clans = get_clans()
	try: clan_tag = clan_tags[clan]
	except Exception:
		await ctx.send(embed=discord.Embed(title='Incorrect Clan!', 
		description='Please enter the capital two-letter abbreviation for the desired clan. (DZ, GC, etc.)'))
		return
	try: war = await coc_client.get_current_war(clan_tag)
	except Exception:
		await ctx.send('An error occured while trying to fetch the latest war information from CoC API!')
		return
	if war.state == 'notInWar':
		await ctx.send('{} is not currently in war!'.format(clans[clan]))
		return
	info = await get_attack_info(war)
	size = war.team_size
	if war.is_cwl == False: size *= 2
	t = war.end_time.time - datetime.now()
	t_rem = time.gmtime(t.total_seconds())
	prnt = '**{} Stats**\nStars: {}\nDestruction: {}%\nAttacks: {}/{}\n\n'
	c1 = prnt.format(war.clan, info['h_star'], info['h_dest'], info['h_hits'], size)
	c2 = prnt.format(war.opponent, info['e_star'], info['e_dest'], info['e_hits'], size)
	t1 = '**Time Remaining**\n{}'.format(time.strftime('%H hours %M minutes', t_rem))
	e = discord.Embed(title='**{}\tVS.\t{}**'.format(war.clan, war.opponent), description=(c1+c2+t1), color=0x3498db)
	await ctx.send(embed=e)
	return 


async def score_all(ctx):
	clan_tags = get_tags()
	clans = get_clans()
	for clan in clans.keys():
		clan_tag = clan_tags[clan]
		try: war = await coc_client.get_current_war(clan_tag)
		except Exception:
			print('An error occured while trying to fetch the latest war information from CoC API!')
			continue
		if war.state == 'notInWar':
			continue
		info = await get_attack_info(war)
		size = war.team_size
		if war.is_cwl == False: size *= 2
		t = war.end_time.time - datetime.now()
		t_rem = time.gmtime(t.total_seconds())
		prnt = '**{} Stats**\nStars: {}\nDestruction: {}%\nAttacks: {}/{}\n\n'
		c1 = prnt.format(war.clan, info['h_star'], info['h_dest'], info['h_hits'], size)
		c2 = prnt.format(war.opponent, info['e_star'], info['e_dest'], info['e_hits'], size)
		t1 = '**Time Remaining**\n{}'.format(time.strftime('%H hours %M minutes', t_rem))
		e = discord.Embed(title='**{}\tVS.\t{}**'.format(war.clan, war.opponent), description=(c1+c2+t1), color=0x3498db)
		await ctx.send(embed=e)
	return


async def get_attack_info(war):
	info = dict(
		h_star = 0, e_star = 0,
		h_dest = 0, e_dest = 0,
		h_hits = 0, e_hits = 0 )
	for attack in war.attacks:
		if attack.attacker.clan.tag == war.clan.tag:
			info['h_star'] += attack.stars
			info['h_dest'] += attack.destruction
			info['h_hits'] += 1
		else:
			info['e_star'] += attack.stars
			info['e_dest'] += attack.destruction
			info['e_hits'] += 1
	info['h_dest'] = round((info['h_dest'] / war.team_size), 2)
	info['e_dest'] = round((info['e_dest'] / war.team_size), 2)
	return info

# ===========================================================
# Tournament Roles
# ===========================================================

async def give_tournament_roles(ctx, client):
	guild = client.get_guild(guild_id)
	try: roles = get_roles(guild)
	except Exception: await ctx.send('Error getting roles from ID!')
	
	data = pd.read_csv('tourn.csv')
	db = pd.read_csv('db.csv')

	tags = []
	for key, val in data.iterrows():
		tags.append(val[0].upper())

	accs_linked = 0
	failed_players = []
	for tag in tags:
		try: 
			id = db.loc[db['player_tag'] == tag]['discord_id'].item()
			th = db.loc[db['player_tag'] == tag]['town_hall'].item()
		except ValueError:
			print('Failed to locate {} in the database!'.format(tag))
			failed_players.append(tag)
		try: user = guild.get_member(id)
		except Exception: 
			print('Error retrieving {} profile from ID!'.format(tag))
			failed_players.append(tag)
		try: role = roles[('TH'+str(th))]
		except KeyError: print('Townhall level {} doesn\'t exist in DB!{}'.format(('TH'+str(th)), tag))
		try: await user.add_roles(role)
		except Exception: 
			print('Failed to give {} roles!'.format(tag))
			failed_players.append(tag)
		accs_linked += 1
	await ctx.send(embed=discord.Embed(title='Tournament roles assigned to {} players!'.format(accs_linked), description='Failed to assign roles to the following tags:\n{}'.format('\n'.join(failed_players))))

	return
