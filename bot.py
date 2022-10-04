
from http import client
import discord
from discord.ext import commands
from game_engine import Player, Game


class Client(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='`', intents=intents)
members = [] # basically a string interpertation of the users
server = None
game = None

@bot.event
async def on_ready():
    global server
    global members

    server = bot.get_guild(1025162671068303391)
    print(f'We have logged in as {bot.user} in Server: {server.name}')
    for i in server.members: 
        members.append(Player(i.id,i.name,i.discriminator))
        


@bot.command()
async def complete(ctx): 
    player = game.completeContract(ctx.message.author.id, ctx.message.content[-3:])
    
    if player is None: 
        await ctx.send("That is not the right player")
    
    await ctx.send(f"Your new target is {player.getTarget()}")

@bot.command()
async def ping(ctx):
    await ctx.send("pong")

@bot.command() 
async def w(ctx): 
    #584825567208144917
    members.__delitem__(0) #removing the first attribute which is the bot itself
    global game
    game = Game(members)
    copy = game.newGame()
    await ctx.send("Assigning Targets...")
    
    for m in copy: 
        user = bot.get_user(m.getId())
        await user.send(f"Your Target is {str(m.getTarget())}")

    await ctx.send("Targets Assigned, Good luck...")
    #print(game)
    print(game._contracts())


    # user = bot.get_user(ID) -> test for single member messaging
    # await user.send('Uwu')
    # print(members)



bot.run('###')
