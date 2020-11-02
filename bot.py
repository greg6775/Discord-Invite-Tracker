# Copyright: GregTCLTK 2018-2020.
# Contact Developer on https://discord.gg/Vf4zCYn (Skidder#5386)

import discord
import asyncio
import datetime
import json
import os

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

async def fetch():
 global last
 global invites
 await client.wait_until_ready()
 gld = client.get_guild(int(guild_id))
 logs = client.get_channel(int(logs_channel))
 while True:
  invs = await gld.invites()
  tmp = []
  for i in invs:
   for s in invites:
    if s[0] == i.code:
     if int(i.uses) > s[1]:
      usr = gld.get_member(int(last))
      eme = discord.Embed(description = "Just joined the server", color = 0x03d692, title = " ")
      eme.set_author(name = usr.name + "#" + usr.discriminator, icon_url = usr.avatar_url)
      eme.set_footer(text = "ID: " + str(usr.id))
      eme.timestamp = usr.joined_at
      eme.add_field(name = "Used invite", value = "Inviter: " + i.inviter.mention + " (`" + i.inviter.name + "#" + i.inviter.discriminator + "`)\nCode: `" + i.code + "`\nUses: `" + str(i.uses) + "`", inline = False)
      await logs.send(embed = eme)
   tmp.append(tuple((i.code, i.uses)))
  invites = tmp
  await asyncio.sleep(4)


@client.event
async def on_ready():
 print("ready!")
 await client.change_presence(activity = discord.Activity(name = "joins", type = 2))


@client.event
async def on_member_join(meme):
 global last
 last = str(meme.id)




client.loop.create_task(fetch())
client.run(token)
