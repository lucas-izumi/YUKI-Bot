import discord
import os
import config as CONFIG
from discord.ext.commands import Bot

intents = discord.Intents.default()
intents.members = True
client = Bot(command_prefix="$", pm_help = False, intents=intents,)
rolelist_ = [0,0,0]
guild_id_ = 0

@client.event
async def on_ready():
  global rolelist_
  global guild_id_
  config_list = CONFIG.readFromFile()
  rolelist_ = config_list[1].replace("[", "").replace("]", "").split(", ")
  guild_id_ = config_list[0]
  print('Yuki is online.')
  activity = discord.Game(name="Aprendendo...")
  await client.change_presence(status=discord.Status.online, activity=activity)

@client.event
async def on_message(message):
  global rolelist_
  global guild_id_
  guild_id_ = message.guild.id

  if message.author == client.user:
    return

  if message.content.startswith('$combineroles'):
    if message.author.top_role.permissions.administrator:
      rolelistnames = message.content.split("\"")[1:6]
      if len(rolelistnames) != 5:
        await message.channel.send('Sintaxe: $combineroles "cargo1" "cargo2" "cargocombinado"')
      else:
        rolelist_ = [0,0,0]
        for role in client.get_guild(guild_id_).roles[1:]:
          if role.name == rolelistnames[0]:
            rolelist_[0] = role.id
          elif role.name == rolelistnames[2]:
            rolelist_[1] = role.id
          elif role.name == rolelistnames[4]:
            rolelist_[2] = role.id

        if any(v == 0 for v in rolelist_):
          await message.channel.send("Não foi possível encontrar um dos cargos!")
          return
        await message.channel.send("**" + rolelistnames[4] + "**" + " agora é uma combinação dos cargos **" + rolelistnames[0] + "** e **" + rolelistnames[2] + "**")
        CONFIG.writeToFile([guild_id_, rolelist_])

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