import discord
import random
import asyncio
from discord.ext import commands,tasks
from discord.ext.commands import Bot, has_permissions, CheckFailure
from itertools import cycle
import os

client = commands.Bot(command_prefix = ']')
status = cycle(['NODES', 'MODULES', 'WAVES'])


# Initalizes the bot and gives it a status
@client.event 
async def on_ready():
    change_status.start()
    print("Bot is online.")

# Backgrounds tasks for the Discord Bot ()
@tasks.loop(seconds=100000)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))

# These commands load and Unload the cogs from ./cogs folder
@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    

@client.command()
async def unload(ctx, extension):
     client.unload_extension(f'cogs.{extension}')

@client.command()
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')

# Searches for the python scripts in the directory and attaches a string to them
for filename in os.listdir('./cogs'):
    if filename.endswith ('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')



@client.event
async def on_memberjoin(member):
    print(f'{member} has joined the server, Welcome!')

@client.event
async def on_member_remove(member):
    print(f'{member} has left the server, Goodbye.')

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! `{round(client.latency * 1000)}ms`')

@client.command(aliases = ['8ball', 'eightball'])
async def _8ball(ctx, *, question):
     responses = ['It is certain.',
 'For sure', 'without a doubt', 'Yes definitely', 'Chances are low', 'Wouldnt count on it.', 'Nope', 'Try again', 'Think hard and try again', 'Go away before I eat your cat', 'I thought too hard and died.']
     await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

@client.command(aliases = ['bot'])
async def info(message):
     embedVar = discord.Embed(title="🎇CodenBot", description="Developed by `Abraham/CodeProductions`, this simple bot was coded with discord.py. This bot is a multi-purpose bot used for administration and chat moderation.", color=0x8919cf)
     embedVar.add_field(name="Documentation and Issues", value="If you run into any issues, please go to the following github: \n https://github.com/Rezatachi", inline=False)
     embedVar.set_thumbnail(url="https://cdn.discordapp.com/attachments/761256129191477261/779902108920709141/Ten.jpg")
     await message.channel.send(embed=embedVar)

@client.command(aliases = ['commands'])
async def ask(message):
    embedHelp = discord.Embed(title="This Embed contains the list of commands for Coden.", description="This bot uses the prefix `]`",color=0x8919cf)
    embedHelp.add_field(name = "Command and Intents", value= "`commands` - displays the help embed displaying the various commands\n  `info` - shows the bot information \n `clear` auto purges messages up to 10 \n `8ball` - fun minigame to test your luck\n  `ban`- bans are member from the discord server\n  `kick`- kicks a member from the server.")
    embedHelp.set_thumbnail(url="https://cdn.discordapp.com/attachments/761256129191477261/779902108920709141/Ten.jpg")
    await message.channel.send(embed=embedHelp)
   

@client.command()
async def clear(ctx, amount : int):
    await ctx.channel.purge(limit=amount)
    embedClear = discord.Embed(title=f'**{amount} messages have been cleared!**')
    botclear = await ctx.channel.send(embed=embedClear)
    await asyncio.sleep(1)
    await botclear.delete()

# Clear error displayed
@clear.error
async def clear_error(ctx, error):
     if isinstance(error, commands.MissingRequiredArgument):
       embedArguement = discord.Embed(title="**Please specify the amount of messages to delete**!")
       botembedArguement = await ctx.channel.send(embed=embedArguement)
       await asyncio.sleep(1)
       await botembedArguement.delete()
    
@client.command()
@commands.has_permissions(kick_members=True)
async def kick(message, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)
    embedVar2 = discord.Embed(title="**User kicked!**", color=0x8919cf)
    botembed = await message.channel.send(embed=embedVar2)
    await asyncio.sleep(2)
    await botembed.delete()

  
@client.command()
@commands.has_permissions(ban_members=True)
async def ban(message, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    embedVar2 = discord.Embed(title="**User banned!**", color=0x8919cf)
    botembedvar = await message.channel.send(embed=embedVar2)
    await asyncio.sleep(2)
    await botembedvar.delete()

    


            
      





 

    

client.run('Nzg1OTQzNjkzMjQ0NzYwMDk0.X8_NGg.1fKGMBpLXwUjoKMcBlqMYYLtMZo')





