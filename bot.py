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
members = []
dead = []
roles = []

server = None
game = None
is_over = False
main_channel = None

@bot.event
async def on_ready():
    global server
    global members
    global main_channel
    
    server = bot.get_guild(1025162671068303391)
    main_channel = bot.get_channel(1025162671538057306)
    print(f'We have logged in as {bot.user} in Server: {server.name}')
    print(f"General Channel for {server.name} is denoted as: {main_channel.name}")

    for i in server.members: 
        members.append(Player(i.id,i.name,i.discriminator))
        


@bot.command()
async def complete(ctx):
    '''Checks if the player who is invoking the command is actually terminating the right target''' 
    global game, dead, is_over, main_channel

    player = game.completeContract(ctx.message.author.id, ctx.message.content[-3:])
    if player[0].isEmpty(): 
        is_over = True
        await main_channel.send(f"{player[1]} has died")
        await ctx.send(f'Congratulations! You win!!') #dm to winner of the game
        await main_channel.send(f'Game Over, winnner is {player[1]}')
        dead = []

        game = None
        is_over = False
               
    else:
        if player is None:
            await ctx.send("That is not the right player")
        else:
            for m in members: 
                if player[1] == m: 
                    user = bot.get_user(m.getId())
                    await user.send(f"A dead man tells no tales... thanks for playing! Enjoy the rest of the game")
            await main_channel.send(f"{player[1]} has died, {game.active} players left")
            await ctx.send(f"Your new target is {player[0].getTarget()}")


@bot.command() 
async def test(ctx): #start command
    #584825567208144917
    # user = bot.get_user(584825567208144917)
    # await user.send('Uwu')
    # print(members)
    pass

@bot.command()
async def start(ctx): 
    '''only admins are allowed to use this command'''
    global game, members

    if game is None : 
        members.__delitem__(0) #removing the first attribute which is the bot itself

        game = Game(members)
        members = game.assignContracts()
        
        print(game._contracts())
        
        await ctx.send("Assigning Targets...")
        for m in members: 
            user = bot.get_user(m.getId())
            await user.send(f"Your Target is {str(m.getTarget())}")
        
        await ctx.send("Targets Assigned, Good luck...")
    else: 
        await ctx.send("A game is already in progress")

@bot.command()
async def endgame(ctx): 
    '''only admins are allowed to use this command'''
    global game, dead, is_over

    game, dead, is_over = None, [], False

    await ctx.send("All contracts deactivated, thank you for playing")

# @bot.command()
# async def rules(ctx): 
#     '''returns the stats of the game'''
#     pass

# @bot.command()
# async def cmds(ctx): 
#     '''returns the commands of the game'''
#     pass

# @bot.command()
# async def help(ctx):
#     pass

bot.run('TOKEN')
