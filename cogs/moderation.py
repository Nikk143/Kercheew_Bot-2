import discord
import asyncio
from discord.ext import commands



class Moderation(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(name="register", aliases=["reg"], description="Using this command creates a dedicated channel for the user.")
  async def create_channel(self, ctx):
    guild = ctx.message.guild
    category_name = "Sector 3"
    category = discord.utils.get(ctx.guild.categories, name=category_name)
    channel_name = str(ctx.message.author).split("#")[0] + "-bots"


    channel_list = ([channel.name for channel in guild.channels])


    if channel_name.lower() in channel_list:
      await ctx.send(f"{channel_name} already exists.")
    

    else:
      await guild.create_text_channel(channel_name, category=category)
      await ctx.send(f"{channel_name} registered successfully!")



  @commands.command(name="delist")
  async def delist(self, ctx):
    guild = ctx.message.guild
    channel_id = ""
    channel_name = str(ctx.message.author).split("#")[0] + "-bots"
    channel_list = ([i.name for i in guild.channels])
    for channel in ctx.guild.channels:
      if channel.name == channel_name.lower():
        channel_id = channel.id

    if channel_name.lower() not in channel_list:
      await ctx.send("User is not registered.")

    else:
      channel = self.bot.get_channel(channel_id)
      await channel.delete()
      await ctx.send("User successfully delisted.")



  @commands.command(pass_context=True)
  @commands.has_permissions(manage_messages=True)
  async def clear(self, ctx, limit: int):
    await ctx.channel.purge(limit=limit+1)
    await ctx.send('Cleared by {}'.format(ctx.author.mention))
    await asyncio.sleep(3)
    await ctx.channel.purge(limit=1)


  @clear.error
  async def clear_error(self, ctx, error):
    if isinstance(error, commands.MissingPermissions):
      await ctx.send("You don't have enough permissions.")


  @commands.command(name="kick", aliases =["yeet"])
  @commands.has_permissions(kick_members=True)
  async def kick(self, ctx, user: discord.Member, *, reason=None):
    await user.kick(reason=reason)
    await ctx.send(f"{user} has been kicked.")


  @kick.error
  async def kick_error(self, ctx, error):
    if isinstance(error, commands.MissingPermissions):
      await ctx.send("You do not have permissions")
    else:
      await ctx.send("User is a Mod/Admin.")




  @commands.command(name="mute", description="Mutes the specified user.")
  @commands.has_permissions(manage_messages=True)
  async def mute(self, ctx, member: discord.Member, *, reason=None):
    if member.guild_permissions.administrator:
      return
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")

    if not mutedRole:
      mutedRole = await guild.create_role(name="Muted")

      for channel in guild.channels:
        await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)
    embed = discord.Embed(title="muted", description=f"{member.mention} was muted ", colour=discord.Colour.red())
    embed.add_field(name="reason:", value=reason, inline=False)
    await ctx.send(embed=embed)
    await member.add_roles(mutedRole, reason=reason)
    await member.send(f" you have been muted from: {guild.name} reason: {reason}")




  @commands.command(name="unmute", description="Unmutes a specified user.")
  @commands.has_permissions(manage_messages=True)
  async def unmute(self, ctx, member: discord.Member):
     mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

     await member.remove_roles(mutedRole)
     await member.send(f" you have unmutedd from: - {ctx.guild.name}")
     embed = discord.Embed(title="unmute", description=f" unmuted-{member.mention}",colour=discord.Colour.light_gray())
     await ctx.send(embed=embed)
      

  @commands.command(name="membercount")
  async def membercount(self, ctx):
    membercount = len([m for m in ctx.guild.members if not m.bot])
    total = len(ctx.guild.members)
    bots = total-membercount
  
    em=discord.Embed(title="Member Count", color=discord.Color.blue())
    em.add_field(name="Members:", value=membercount)
    em.add_field(name="Bots:", value=bots)
    em.add_field(name="Total:", value=total)
    await ctx.send(embed=em)
   



def setup(bot):
  bot.add_cog(Moderation(bot))