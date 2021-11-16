import discord
import random
import api_usage
import asyncio
from discord.ext import commands



class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name='coinflip', aliases=['cf'])
    async def coinflip(self, ctx):
        coin = ["Heads", "Tails"]
        await ctx.send(random.choice(coin))
        

    @commands.command(name='joke')
    async def send_joke(self, ctx):
        try:
            await ctx.send(embed = discord.Embed(title="Joke"                                            , url="", description=api_usage.get_joke(), color=discord.Color.red()))

        except:
            await ctx.send("Something went wrong. Please try again.")

    @commands.command(name='meme')
    async def send_meme(self, ctx):
        try:
            await ctx.send(embed = discord.Embed(title="Memes"                                            , url="", description=api_usage.get_meme(), color=discord.Color.blue()))

        except:
            await ctx.send("Something went wrong. Please try again.")



    @commands.command(name="quote")
    async def send_quote(self, ctx):
        await ctx.send(embed = discord.Embed(title="quote", description=api_usage.get_quote(), color=discord.Color.red()))



    @commands.command(name="bubblewrap", aliases=["bw"])
    async def bubblewrap(self, ctx):
        await ctx.send("""       ||pop||||pop||||pop||
    ||pop||||pop||||pop||
    ||pop||||pop||||pop||""")



    @commands.command(name="dice_roll", aliases=["dr"])
    async def roll_dice(self, ctx):
        number = random.randint(1, 6)
        await ctx.send(number)



    
    @commands.command(name="guess_the_number", aliases=["gtn"])
    async def gtn(self, ctx):
        number = random.randint(0, 10)
        attempts = 3
        await ctx.send("Enter your guess between 0-10.")

        def check(m: discord.Message):
            return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id
        
        
        for i in range(3):
            attempts -= 1
            try:
                response = await self.bot.wait_for(event='message', check=check, timeout=10.0)
            except asyncio.TimeoutError:
                await ctx.send("You didn't respond in time.")
            else:
                guess = int(response.content)
                if guess is number:
                    await ctx.send("You guessed the number!")
                    return
                elif attempts:
                    await ctx.send(f"You failed to guess the number. You have {attempts} attempt(s) left now.")
                else:
                    await ctx.send(f"You weren't able to guess the number. The number was `{number}`")




    @commands.command(name='8ball', aliases=["8b"])  
    async def ball(self, ctx):
        info = ["It is certain", "Of course", "Wihout a doubt", "Yes", "Defenitely yes", "Most likely", "Idk", "I don't care", "Better not tell you now", "NOOOOO", "Of course not, you dummy", "What did you expect?", "My reply is no", "The gods said no"]
        await ctx.send(random.choice(info))
  



    @commands.command(name="kill")
    async def shoot(self, ctx, member: discord.Member):
        user = str(member).split("#")[0]
        outputs = [f"{user} is dead.", f"{user} is down.", f"{user} was killed by drugs", f"{user} was shot by the Uruk-hai and died of exessive blood loss.", f"{user} got hit by a car and died.", f"{user} drank too much alcohol and died on the way back home.", f"Voldemort used Avada Kedavra on {user} and succeed. {user} died.", f"{user} fell from a tall building and landed on the wrong platform.", f"{user} ate too much and died of diabetes.", f"{user} got stuck inside a box and died of suffocation.", f"{user} got spotted by the Barad-dûr and died in the hands of Sauron.", f"The doctor accidentally left a scissors in {user}'s stomach. {user} died. ", f"{user} get reaped from behind" f"{user} get squashed by a bunch of library books", f"{user} can't withstand the fire of a Charizard. {user} died" ]

        await ctx.send(random.choice(outputs), delete_after=5)
        

    @commands.command(name="shout")
    async def shout(self, ctx):
      await ctx.send(ctx.upper())

 

    

 
  


def setup(bot):
    bot.add_cog(Fun(bot))