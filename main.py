import discord
import os

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)
rolelist_ = [0,0,0]
guild_id_ = 0

@client.event
async def on_ready():
  print('Yuki is online.')

@client.event
async def on_message(message):
  global rolelist_
  global guild_id_
  if message.author == client.user:
    return
  
  if message.content.startswith('$hello'):
    await message.channel.send('Hello!')

  if message.content.startswith('$combineroles'):
    guild_id_ = message.guild.id
    # necessario dar suporte a cargos com espaco no nome
    # criar persistencia
    rolelistnames = message.content.replace("\"", "").split()[1:]
    if len(rolelistnames) != 3:
      await message.channel.send('Sintaxe: $combineroles "cargo1" "cargo2" "cargocombinado"')
    else:
      for role in client.get_guild(guild_id_).roles:
        if role.name == rolelistnames[0]:
          rolelist_[0] = role.id
        elif role.name == rolelistnames[1]:
          rolelist_[1] = role.id
        if role.name == rolelistnames[2]:
          rolelist_[2] = role.id
      await message.channel.send("**" + rolelistnames[2] + "**" + " agora é uma combinação dos cargos **" + rolelistnames[0] + "** e **" + rolelistnames[1] + "**")

@client.event
async def on_member_update(before, after):
  global rolelist_
  count = 0
  for rl in rolelist_:
    for r in after.roles:
      if str(rl) == str(r.id):
        count += 1
  if (count == 2):
    myGuild = client.get_guild(guild_id_);
    myRole = myGuild.get_role(int(rolelist_[2]))
    await after.add_roles(myRole)
  # remover o cargo conjunto caso um dos cargos seja removido

client.run(os.getenv('BOT_TOKEN'))