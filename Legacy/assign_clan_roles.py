@commands.command(name='buildroles')
    @commands.has_permissions(administrator=True)
    async def build_roles(self, ctx):
        msg = await ctx.send(embed=discord.Embed(title='Assigning Roles!', color=0xf1c40f,
                                                 description='Hang tight, This operation may take several minutes.'))
        db, cursor = await self.connect_db()
        guild = self.client.get_guild(self.client.guild)
        dz = await guild.get_role(819709187302359059)
        dl = await guild.get_role(858006003042746399)
        cwl = pd.read_csv('players.csv')

        failed = []
        for clan, player_list in cwl.iteritems():
            for player in player_list:
                if pd.isna(player):
                    continue
                cursor.execute('SELECT discord_id FROM linked_accounts WHERE player_tag = "{}"'.format(player))
                result = cursor.fetchone()
                if not result:
                    failed.append(player)
                    continue
                try:
                    user = guild.get_member(result[0])
                    if clan is 'DZ':
                        await user.add_roles(dz)
                    elif clan is 'DL':
                        await user.add_roles(dl)
                    else:
                        print(f'Failed on {user}')
                except Exception:
                    failed.append(player)
                    continue
        if failed:
            players = [(await self.client.coc.get_player(tag)).name for tag in failed]
            failmsg = [tag + ' - ' + name for (tag, name) in zip(failed, players)]
            return await msg.edit(embed=discord.Embed(title='Roles Assigned!', color=0x287e29,
                                                      description='Role assignment failed on:\n{}'
                                                      .format('\n'.join(failmsg))))
        return await msg.edit(embed=discord.Embed(title='Roles Assigned!', color=0x287e29))
