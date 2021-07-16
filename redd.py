# ====================================
nr_subred_ch_id = 675444353237516314
ph_subred_ch_id = 819709189181800481
reminder_ch_id = 819709189181800480
# ====================================
import datetime

dfr = {'Danger Zone': 610688204395380757,        # Michael
       'Stormcloaks': 323148470376726551,        # Ice
       'Downfall Legend': 7748683076225204326,   # SparkPlug
       'Game Changers': 323148470376726551,      # Ice
       'Beasthole': 395777730492235777,          # Peter
       'Phantom Family': 610688204395380757,     # Michael
       'Night Raiderz': 384491690410639370       # John
      }

async def check_subred(ctx, client):
	if ctx.channel.id != nr_subred_ch_id or not ctx.embeds:
		return
	channel = client.get_channel(ph_subred_ch_id)
	for embed in ctx.embeds:
		await channel.send(embed=embed)
	return


async def reminder(client):
	df = list(dfr.items())
	day = datetime.datetime.today().weekday()
	data = df[day]  # Tuple(clan,id)
	channel = client.get_channel(reminder_ch_id)
	rc = client.get_user(data[1])
	await channel.send('\n**Recruitment Post Reminder**\nPlease post for {} {}'.format(data[0], rc.mention))
	return