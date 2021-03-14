import discord

async def checkroles(ctx, raw_roleID):
	roleID = raw_roleID.translate({ord(i): None for i in '<@&>'})
	if roleID == 'none' or roleID == 'None' or roleID == 'NONE':
		members = await get_members_nr(ctx, [])
		return await ctx.send(embed=discord.Embed(title='Users with No Role', description="\n".join(members)))
	
	try: role = ctx.guild.get_role(int(roleID))
	except ValueError:
		return await ctx.send(embed=discord.Embed(description="That role does not exist in this server!"))
	
	if not role.members: 
		return await ctx.send(embed=discord.Embed(description="The role {} is assigned to zero users!".format(role.mention)))
	return await print_members(ctx, role, await get_members(role, []), [])


async def get_members(role, members):
	for member in role.members:
		if member.nick != None:
			members.append("{}#{} ({})".format(member.name, member.discriminator, member.nick))
			continue
		members.append("{}#{}".format(member.name, member.discriminator))
	return members


async def get_members_nr(ctx, members):
	for member in ctx.guild.members:
		if len(member.roles) <= 1:	
			if member.nick != None:
				members.append("{}#{} ({})".format(member.name, member.discriminator, member.nick))
				continue
			members.append("{}#{}".format(member.name, member.discriminator))
	return members


async def print_members(ctx, role, members, tmp_list):
	if len(members) <= 80:
		return await ctx.send(embed=discord.Embed(title="Users with @{}".format(role), description="\n".join(members)))
	for member in members:
		tmp_list.append(member)
		if len(tmp_list) == 80:
			await ctx.send("\n".join(tmp_list))
			tmp_list = []
	await ctx.send("\n".join(tmp_list))