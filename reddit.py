import pandas as pd
# ====================================
#     Check Subreddit ID's
nr_subred_ch_id = 675444353237516314
ph_subred_ch_id = 819709189181800481
# ====================================
#     Recruitment Reminder ID's
reminder_ch_id = 819709189181800480
# ====================================

async def check_subred(ctx, client):
	if ctx.channel.id != nr_subred_ch_id or not ctx.embeds:
		return
	channel = client.get_channel(ph_subred_ch_id)
	for embed in ctx.embeds:
		await channel.send(embed=embed)
	return


async def red_reminder(client):
	df = pd.read_csv('reddit_reminders.csv')
	row = df.loc[df['active'] == True]
	day = int(row['day'])
	channel = client.get_channel(reminder_ch_id)
	rc1 = client.get_user(int(row['rc1_id']))
	rc2 = client.get_user(int(row['rc2_id']))
	await channel.send('\n**Recruitment Post Reminder - Day {}**\n{} please post for {}\n{} please post for {}'.format(day, rc1.mention, row['clan1'].item(), rc2.mention, row['clan2'].item()))
	df['active'] = False
	day += 1
	if day > 6: day = 1
	df.loc[df.day == day, 'active'] = True
	df.to_csv('reddit_reminders.csv', index=False)
	return