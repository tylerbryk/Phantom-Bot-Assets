# =============== GLOBAL VARIABLES ===================
messageID    = 852646562114961469
dz_channel   = 819709187822583813
dl_channel   = 819709187822583816
gc_channel   = 819709187822583814
welc_channel = 819709187822583812
roleID_dzRc  = '<@&819709187285975073>'
roleID_dlRc  = '<@&819709187285975071>'
roleID_gcRc  = '<@&819709187285975072>'
roleID_gaRc  = '<@&819709187285975070>'
server_rules = '<#819709187613392913>'
dz_rules     = '<#819709187613392914>'
dl_rules     = '<#819709187822583808>'
gc_rules     = '<#819709187613392915>'
dz_emoji     = 852634339844816966
dl_emoji     = 858033764453580820
gc_emoji     = 852634339954917466
ga_emoji     = 820103306604707860
# =====================================================

async def applicant_ping(ctx, client):
	if ctx.message_id != messageID:
		return

	message = "{} is applying for **{}**\n\nPlease do the following:\n1. Read the {} and {}\n2. Send a screenshot of your base\n3. Send a screenshot of your profile\n4. Send your player tag (Ex: #5GC47AE)\n\nA {} will be online to assist you shortly!"
	
	if ctx.emoji.id == dz_emoji:
		channel = client.get_channel(dz_channel)
		await channel.send(message.format(ctx.member.mention, 
																			'Danger Zone', server_rules, dz_rules, roleID_dzRc))
	elif ctx.emoji.id == dl_emoji:
		channel = client.get_channel(dl_channel)
		await channel.send(message.format(ctx.member.mention, 
																			'Downfall Legend', server_rules, dl_rules, roleID_dlRc))
	elif ctx.emoji.id == gc_emoji:
		channel = client.get_channel(gc_channel)
		await channel.send(message.format(ctx.member.mention, 
																			'Game Changers', server_rules, gc_rules, roleID_gcRc))
	elif ctx.emoji.id == ga_emoji:
		channel = client.get_channel(welc_channel)
		await channel.send('{} is a **General Applicant**\n\nPlease do the following:\n1. Read the {}\n2. Send a screenshot of your base\n3. Send a screenshot of your profile\n4. Send your player tag (Ex: #5GC47AE)\n\nA {} will be online to assist you shortly!'.format(ctx.member.mention, server_rules, roleID_gaRc))
	else:
		channel = client.get_channel(welc_channel)
		await channel.send('{} reacted with an invalid option!\nPlease visit {} and select a clan application type!'.format(ctx.member.mention, server_rules))