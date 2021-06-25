# ====================================
nr_subred_ch_id = 675444353237516314
ph_subred_ch_id = 819709189181800481
reminder_ch_id = 819709189181800480
# ====================================

import datetime
import pandas as pd

async def check_subred(ctx, client):
	if ctx.channel.id != nr_subred_ch_id or not ctx.embeds:
		return
	channel = client.get_channel(ph_subred_ch_id)
	for embed in ctx.embeds:
		await channel.send(embed=embed)
	return


async def reminder(client):
	df = pd.read_csv('reddit_reminders.csv')
	day = df.loc[df['day'] == datetime.datetime.today().weekday()]
	channel = client.get_channel(reminder_ch_id)
	rc = client.get_user(int(day['rc_id']))
	await channel.send('\n**Recruitment Post Reminder**\nPlease post for {} {}'.format(day['clan'].item(), rc.mention))
	return