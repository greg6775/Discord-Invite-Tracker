# Copyright: GregTCLTK 2018-2021.
# Contact Developer on https://discord.gg/nPwjaJk (Skidder#8515 | 401817301919465482)
# Cog by: Quill (quillfires)

import discord
import asyncio
import json
import time
import typing
import datetime
from discord.ext import commands
# from discord.ext.commands import has_permissions
from discord import Embed

cfg = open("config.json", "r")
tmpconfig = cfg.read()
cfg.close()
config = json.loads(tmpconfig)

class invite_tracker(commands.Cog):
    """
    Keep track of your invites
    """
    def __init__(self, bot):
        self.bot = bot
        self.logs_channel = config["logs-channel-id"]
        self.version = "1.0.0"

        self.invites = {}
        bot.loop.create_task(self.load())

    async def load(self):
        await self.bot.wait_until_ready()
        # load the invites
        for guild in self.bot.guilds:
            try:
                self.invites[guild.id] = await guild.invites()
            except:
                pass

    def find_invite_by_code(self, inv_list, code):
        for inv in inv_list:
            if inv.code == code:
                return inv

    @commands.Cog.listener()
    async def on_member_join(self, member):
        logs = self.bot.get_channel(int(self.logs_channel))
        eme = Embed(description="Just joined the server", color=0x03d692, title=" ")
        eme.set_author(name=str(member), icon_url=member.avatar_url)
        eme.set_footer(text="ID: " + str(member.id))
        eme.timestamp = member.joined_at
        try:
            invs_before_join = self.invites[member.guild.id]
            invs_after_join = await member.guild.invites()
            for invite in invs_before_join:
                if invite.uses < find_invite_by_code(invites_after_join, invite.code).uses:
                    eme.add_field(name="Used invite",
                                  value=f"Inviter: {invite.inviter.mention} (`{invite.inviter}` | ` {str(invite.inviter.id)} )`\nCode: `{invite.code} `\nUses: ` {str(invite.uses)}", inline=False)
        except:
            pass
        await logs.send(embed=eme)
        self.invites[member.guild.id] = invs_after_join
        return

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        logs = self.bot.get_channel(int(self.logs_channel))
        eme = Embed(description="Just left the server", color=0xff0000, title=" ")
        eme.set_author(name=str(member), icon_url=member.avatar_url)
        eme.set_footer(text="ID: " + str(member.id))
        eme.timestamp = member.joined_at
        try:
            invs_before_rem = self.invites[member.guild.id]
            invs_after_rem = await member.guild.invites()
            for invite in invs_before_rem:
                if invite.uses > find_invite_by_code(invites_after_rem, invite.code).uses:
                    eme.add_field(name="Used invite",
                                  value=f"Inviter: {invite.inviter.mention} (`{invite.inviter}` | ` {str(invite.inviter.id)} )`\nCode: `{invite.code} `\nUses: ` {str(invite.uses)}", inline=False)
        except:
            pass
        await logs.send(embed=eme)
        self.invites[member.guild.id] = await member.guild.invites()
        return

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        try:
            self.invites[guild.id] = await guild.invites()
        except:
            pass

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        try:
            self.invites.pop(guild.id)
        except:
            pass

    # @commands.guild_only()
    # @has_permissions(ban_members=True)
    # async def update(self, ctx):
    #     """Update your cog"""
    #     #

def setup(bot):
    bot.add_cog(invite_tracker(bot))
