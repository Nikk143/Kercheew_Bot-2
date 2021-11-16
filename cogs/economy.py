import discord
import json
import random
import asyncio
from discord.ext import commands



class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.shop = [
      {"name": "Basket", "price": 0, "description": "A brown picnic basket, can be found in the Goose forest, which contains an apple, sandwich, and carrot"},
      {"name": "Sandwich", "price": 0, "description": "A half diagonally cut sandwich. Looking up close you can see lettuce and tomato. Restores 10 hunger points"},
      {"name": "Apple", "price": 0, "description": "A red apple. Restores 2 hunger points."},
      {"name": "Pumpkin", "price": 0, "description": "A standard orange pumpkin (seriously what did you expect). Used to disguise from animals "},
      {"name": "Carrot", "price": 0, "description": "A small carrot. Can be used to poke people and other animals."},
      {"name": "Jam", "price": 0, "description": "A jar of strawberry jam. Restores 10 hunger points."},
      {"name": "Thermos", "price": 0, "description": "A bottle that keeps water warm. Can be thrown at people or animals "},
      {"name": "Radio", "price": 0, "description": "A standard 1900s radio. Used to make the goose *dance*"},
      {"name": "Tulip", "price": 0, "description": "A red tulip. Use to *propose* another goose"},
      {"name": "Shovel", "price": 0, "description": "A grey shovel. Used to dig up treasure."},
      {"name": "Rake", "price": 0, "description": "A green rake with a brown handle. Used for clearing up grass."},
      {"name": "Wooden crate", "price": 0, "description": "A normal wooden crate. Used for sleeping"},
      {"name": "Watering can", "price": 0, "description": "A big blue watering can. Used to grow vegetables."},
      {"name": "Rainboots", "price": 0, "description": "A pair of yellow duck rainboots. Can be used to walk on wAtEr?"},
      {"name": "Mug", "price": 0, "description": "A red mug filled with coffee? Can either restore or decrease 30 energy points."},
      {"name": "Cooler", "price": 0, "description": "A cooler filled with ice. Use to contain bottles"},
      {"name": "Coin", "price": 0, "description": "A GOLDEN COIN. Can be used to redeem 100000 GC"},
      {"name": "Golden Bell", "price": 0, "description": "A big, fat bell. Use to wake everyone up at night"},
      {"name": "Glass bottle", "price": 0, "description": "A greenish glass bottle. Can be used to SMASH at people or wild animals."},
      {"name": "Toy plane", "price": 0, "description": "A red and white plane. Can we fly on it?"},
      {"name": "Wimp's glasses", "price": 0, "description": "When you equip these glasses, you can run away from people. What a wimp!"},
      {"name": "Chalk", "price": 0, "description": "A white chalk. That’s it."},
      {"name": "Canned foods", "price": 0, "description": "FOOD! Restores 50 hunger points."},
      {"name": "Shopping basket", "price": 0, "description": "A wooden pushroom. Used to sweep the dust off people’s faces."},
      {"name": "Pushbroom", "price": 0, "description": "A yellow basket. Did you steal this wtf?"},
      {"name": "Dishwash bottle", "price": 0, "description": "A bottle filled with soap. Used to create a slippery field around people."},
      {"name": "Spray bottle", "price": 0, "description": "A bottle with spray paint. Used to draw stuff on walls"},
      {"name": "Pricing gun", "price": 0, "description": "A powerful black gun. Used to shoot water at people"},
    ]
      
  
    @commands.command(name="balance", aliases=['bal'])
    async def balance(self, ctx, member: discord.Member = None):
        if member == None:
            await Economy.open_account(ctx.author)
            user = ctx.author

            users = await Economy.get_bank_data()

            wallet_amt = users[str(user.id)]["wallet"]
            bank_amt = users[str(user.id)]["bank"]
            bankspace = users[str(user.id)]["bankspace"]

            em = discord.Embed(title=f'{ctx.author.name}\'s Balance',color=discord.Color.dark_grey())
            em.add_field(name="Wallet Balance", value=("{:,}".format(wallet_amt)))
            em.add_field(name='Bank Balance',value=("{:,}".format(bank_amt) + " / " + "{:,}".format(bankspace)))
            await ctx.send(embed= em)
        else:
            await Economy.open_account(member)
            user = member
            users = await Economy.get_bank_data()

            wallet_amt = users[str(user.id)]["wallet"]
            bank_amt = users[str(user.id)]["bank"]
            bankspace = users[str(user.id)]["bankspace"]

            em = discord.Embed(title=f'{member.name}\'s Balance',color = discord.Color.dark_gray())
            em.add_field(name="Wallet Balance", value=("{:,}".format(wallet_amt)))
            em.add_field(name='Bank Balance',value=("{:,}".format(bank_amt) + "/" + "{:,}".format(bankspace)))
            await ctx.send(embed= em)


    @commands.command(name="give", aliases=["share"])
    async def give(self, ctx, member: discord.Member, amount: int):
	    user = ctx.author
	    user_data = await Economy.get_bank_data()
	    user_wallet = user_data[str(user.id)]["wallet"]
		
	    if amount > user_wallet:
		    await ctx.send("You don't have enough money.")
		    return
			
	    else:
		    await Economy.update_bank(user, -1*amount)
		    await Economy.update_bank(member, amount)
		    await ctx.send("{0} gave {1} {2}".format(ctx.author.mention, member.mention, amount))
    
    

    @commands.command(name="beg")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def beg(self, ctx):
        await Economy.open_account(ctx.author)
        user = ctx.author

        users = await Economy.get_bank_data()

        earnings = random.randrange(101)

        await ctx.send(f'{ctx.author.mention} Got {earnings} coins!!')

        users[str(user.id)]["wallet"] += earnings

        with open("economy.json",'w') as f:
            json.dump(users,f)

    @beg.error
    async def beg_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            em = discord.Embed(title="Cooldown", description="You're on a cooldown for 10s, please try again after {:.2f}s".format(error.retry_after), color=discord.Color.red())
            await ctx.send(embed=em)
  


    @commands.command(name="daily")
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def daily(self, ctx):
        await Economy.update_bank(ctx.author, 2500)
        em = discord.Embed(title="Congratulations!", description="2,500 daily coins claimed successfully, and added to your wallet.", color=discord.Color.blue())

        await ctx.send(embed=em)
            

    @daily.error
    async def daily_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            em = discord.Embed(title="Cooldown", description="You've already claimed your daily rewards. Dont be greedy.", color=discord.Color.red())
            await ctx.send(embed=em)            


    @commands.command(name='withdraw', aliases=['with'])
    async def withdraw(self, ctx, amount = None):
        await Economy.open_account(ctx.author)
        if amount == None:
            await ctx.send("Please enter the amount")
            return

        bal = await Economy.update_bank(ctx.author)
        user_data = await Economy.get_bank_data()
        bank_bal = user_data[str(ctx.author.id)]["bank"]

        if amount == "all" or "max":
            await Economy.update_bank(ctx.author, bank_bal,"wallet")
            await Economy.update_bank(ctx.author, -1*bank_bal, "bank")
            await ctx.send(f'{ctx.author.mention} You withdrew {bank_bal} coins')
            return

      
        amount = int(amount)

        if amount > bal[1]:
            await ctx.send('You do not have sufficient balance')
            return
        if amount < 0:
            await ctx.send('Amount must be positive!')
            return

        await Economy.update_bank(ctx.author,amount)
        await Economy.update_bank(ctx.author,-1*amount,'bank')
        await ctx.send(f'{ctx.author.mention} You withdrew {amount} coins')
      

    @commands.command(name='deposit', aliases=['dep'])
    async def deposit(self, ctx, amount = None):
        await Economy.open_account(ctx.author)

        if amount == None:
            await ctx.send("Please enter the amount")
            return

        bal = await Economy.update_bank(ctx.author)
        user_data = await Economy.get_bank_data()
        bank_amount = user_data[str(ctx.author.id)]['bank']
        wallet_bal = user_data[str(ctx.author.id)]["wallet"]
        bankspace = user_data[str(ctx.author.id)]["bankspace"]
        available_space = bankspace - bank_amount


        if amount == "all" or amount == "max":
            if wallet_bal > available_space:
                await Economy.update_bank(ctx.author, -1*available_space)
                await Economy.update_bank(ctx.author, available_space, "bank")

                await ctx.send(f'{ctx.author.mention} You deposited {available_space} coins')
                return
            else:
                await Economy.update_bank(ctx.author, -1*wallet_bal)
                await Economy.update_bank(ctx.author, wallet_bal, "bank")

                await ctx.send(f'{ctx.author.mention} You deposited {wallet_bal} coins')
                return


        amount = int(amount)
        
        if amount > bal[0]:
            await ctx.send('You do not have sufficient balance')
            return
        if amount < 0:
            await ctx.send('Amount must be positive!')
            return
        
        if amount > available_space:
      	  await ctx.send('You dont hace enough bankspace.')

        else:
            await Economy.update_bank(ctx.author,-1*amount)
            await Economy.update_bank(ctx.author,amount,'bank')
            await ctx.send(f'{ctx.author.mention} You deposited {amount} coins')


  


    @commands.command(name="shop")
    async def shop(self, ctx):
        em = discord.Embed(title="Shop")

        for item in self.shop:
            temp_list = list()
            name = item["name"]
            price = item["price"]
            desc = item["description"]

            em.add_field(name=f"\n{name} — ${price}", value=desc + "\n\u200b")           

        await ctx.send(embed = em)






    async def open_account(user):

        users = await Economy.get_bank_data()

        if str(user.id) in users:
            return False
        else:
            users[str(user.id)] = {}
            users[str(user.id)]["wallet"] = 0
            users[str(user.id)]["bank"] = 0
            users[str(user.id)]["bankspace"] = 10000

        with open('economy.json','w') as f:
            json.dump(users,f)

        return True




    async def get_bank_data():
        with open('economy.json') as f:
            users = json.load(f)

        return users


    async def update_bank(user,change=0,mode = 'wallet'):
        users = await Economy.get_bank_data()

        users[str(user.id)][mode] += change

        with open('economy.json','w') as f:
            json.dump(users,f)
        bal = users[str(user.id)]['wallet'],users[str(user.id)]['bank']
        return bal





def setup(bot):
    bot.add_cog(Economy(bot))