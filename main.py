import discord
import os
import json
import info_cmds
from discord import Intents
from discord.ext import commands
from keep_alive import keep_alive



def load_cogs():
  cogs = ['cogs.moderation',
         'cogs.economy',
         'cogs.fun_cmds']    

  for cog in cogs:
    bot.load_extension(cog)


intents = Intents.default()
intents.members = True


def get_prefix(bot, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f) 
    return prefixes[str(message.guild.id)]


bot = commands.Bot(command_prefix=(get_prefix), intents=intents)



@bot.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = '<'

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)


    with open('welcome_id.json', 'r') as f:
        data = json.load(f)
    data[str(guild.id)] = guild.text_channels[0]

    with open('welcome_id.json', 'w') as f:
        json.dump(data, f, indent=4)

@bot.event
async def on_guild_remove(guild): 
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id)) 

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)
        
        
        
@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def changeprefix(ctx, prefix):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

    await ctx.send(f'Prefix changed to: "`{prefix}`"')



@bot.event
async def on_message(message):
  if bot.user.mentioned_in(message) and message.mention_everyone is False:
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    await message.channel.send(f'My prefix is "`{prefixes[str(message.guild.id)]}`"')
  await bot.process_commands(message)




@bot.event
async def on_ready():
  print(f"Loggined as {bot.user.name}")

  await bot.change_presence(activity=discord.Game("<help | by Kercheew_#3926, Nikk#0261 and minhbilly#0416"), status=discord.Status.online)



@bot.event
async def on_member_join(member):
  with open('welcome_id.json', 'r') as f:
    data = json.load(f)
    channel_id = data[str(member.guild.id)]
  await bot.get_channel(int(channel_id)).send(member.avatar_url)
  await bot.get_channel(int(channel_id)).send(f"Welcome {member.mention}, hope you enjoy your stay.")





class Info(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    
  @commands.command(name="news")
  async def send_news(self, ctx):
    await ctx.send(embed = discord.Embed(title="News", description=info_cmds.news(), color=discord.Color.blue()))


  @commands.command(name="ping")
  async def ping(self, ctx):
    await ctx.send(f'Pong! `{round(bot.latency*1000, 1)}`ms')
  




keep_alive()
load_cogs()
bot.add_cog(Info(bot))
bot.run(os.environ.get("TOKEN"))