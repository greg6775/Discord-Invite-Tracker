# Copyright: GregTCLTK 2018-2021.
# Contact Developer on https://discord.gg/nPwjaJk (Skidder#8515 | 401817301919465482)

import discord
import asyncio
import json

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

cfg = open("config.json", "r")
tmpconfig = cfg.read()
cfg.close()
config = json.loads(tmpconfig)

token = config["token"]
guild_id = config["server-id"]
logs_channel = config["logs-channel-id"]

invites = {}
last = ""

async def load_invs():
    # load the invites
    for guild in client.guilds:
        self.invites[guild.id] = await guild.invites()

def find_invite_by_code(self, inv_list, code):
    for inv in inv_list:
        if inv.code == code:
            return inv

@client.event
async def on_ready():
    print("ready!")
    await client.change_presence(activity=discord.Activity(name="joins", type=2))

@client.event
async def on_member_join(member):
    global invites
    logs = client.get_channel(int(logs_channel))
    invs_before_join = invites[member.guild.id]
    invs_after_join = await member.guild.invites()
    eme = Embed(description="Just joined the server", color=0x03d692, title=" ")
    eme.set_author(name=str(member), icon_url=member.avatar_url)
    eme.set_footer(text="ID: " + str(member.id))
    eme.timestamp = member.joined_at
    for invite in invs_before_join:
        if invite.uses < find_invite_by_code(invites_after_join, invite.code).uses:
            eme.add_field(name="Used invite",
                          value=f"Inviter: {invite.inviter.mention} (`{invite.inviter}` | ` {str(invite.inviter.id)} )`\nCode: `{invite.code} `\nUses: ` {str(invite.uses)}", inline=False)
    await logs.send(embed=eme)
    self.invites[member.guild.id] = invs_after_join
    return

@client.event
async def on_member_remove(self, member):
    global invites
    logs = client.get_channel(int(logs_channel))
    eme = Embed(description="Just left the server", color=0xff0000, title=" ")
    eme.set_author(name=str(member), icon_url=member.avatar_url)
    eme.set_footer(text="ID: " + str(member.id))
    eme.timestamp = member.joined_at
    invs_before_rem = invites[member.guild.id]
    invs_after_rem = await member.guild.invites()
    for invite in invs_before_rem:
        if invite.uses > find_invite_by_code(invites_after_rem, invite.code).uses:
            eme.add_field(name="Used invite",
                          value=f"Inviter: {invite.inviter.mention} (`{invite.inviter}` | ` {str(invite.inviter.id)} )`\nCode: `{invite.code} `\nUses: ` {str(invite.uses)}", inline=False)
    await logs.send(embed=eme)
    self.invites[member.guild.id] = await member.guild.invites()
    return

@client.event
async def on_guild_join(self, guild):
    global invites
    invites[guild.id] = await guild.invites()

@client.event
async def on_guild_remove(self, guild):
    global invites
    try:
        invites.pop(guild.id)
    except:
        pass


client.loop.create_task(load_invs())
client.run(token)
