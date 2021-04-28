import discord
import random
import asyncio
import youtube_dl
from discord.ext import commands, tasks
from discord.utils import get
from discord import FFmpegPCMAudio
from discord.ext.commands import Bot, has_permissions, CheckFailure
from itertools import cycle
from youtube_dl import YoutubeDL
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

KEY = os.environ.get("KEY")

MY_TOKEN_HERE = os.getenv('MY_TOKEN_HERE')
client = commands.Bot(command_prefix=']')
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
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


# When a Member Joins the server,
@client.event
async def on_memberjoin(member):
    print(f'{member} has joined the server, Welcome!')

# When a Members Leaves the server,


@client.event
async def on_member_remove(member):
    print(f'{member} has left the server, Goodbye.')

# Shows the ping of the bot


@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! `{round(client.latency * 1000)}ms`')

# Creates a 8ball minigame with a range of responses from the bot


@client.command(aliases=['8ball', 'eightball'])
async def _8ball(ctx, *, question):
    responses = ['It is certain', 'It is decidedly so', 'Without a doubt', 'Yes – definitely', 'You may rely on it', 'As I see it, yes', 'Most likely', 'Outlook good', 'Yes Signs point to yes', 'Reply hazy',
                 'try again', 'Ask again later', 'Better not', 'Cannot predict now', 'Concentrate and ask again', 'Dont count on it', 'My reply is no', 'My sources say no', 'Outlook not so good', 'Very doubtful']
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

# Info Embed, used for displaying information


@client.command(aliases=['bot'])
async def info(message):
    embedVar = discord.Embed(
        title="🎇CodenBot", description="Developed by `Abraham/CodeProductions`, this simple bot was coded with discord.py. This bot is a multi-purpose bot used for administration and chat moderation.", color=0x8919cf)
    embedVar.add_field(name="Documentation and Issues",
                       value="If you run into any issues, please go to the following github: \n https://github.com/Rezatachi", inline=False)
    embedVar.set_thumbnail(
        url="https://cdn.discordapp.com/attachments/761256129191477261/779902108920709141/Ten.jpg")
    await message.channel.send(embed=embedVar)

# Creates an embed for how many commands there are


@client.command(aliases=['commands'])
async def ask(message):
    embedHelp = discord.Embed(title="This Embed contains the list of commands for Coden.",
                              description="This bot uses the prefix `]`", color=0x8919cf)
    embedHelp.add_field(name="Command and Intents", value="`commands` - displays the help embed displaying the various commands\n  `info` - shows the bot information \n `clear` auto purges messages up to 10 \n `8ball` - fun minigame to test your luck\n  `ban`- bans are member from the discord server\n  `kick`- kicks a member from the server.\n `load` - loads extra commands from cogs \n `play` - playing music from youtube URL \n `leave` - bot leaves the voice channel \n `stop` - music stops playing \n `resume` - music resumes \n `pause` - music is paused. ")
    embedHelp.set_thumbnail(
        url="https://cdn.discordapp.com/attachments/761256129191477261/779902108920709141/Ten.jpg")
    await message.channel.send(embed=embedHelp)

# Clear commands, wont work without numbers


@client.command()
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount)
    embedClear = discord.Embed(
        title=f'**{amount} messages have been cleared!**')
    botclear = await ctx.channel.send(embed=embedClear)
    await asyncio.sleep(1)
    await botclear.delete()

# Clear error displayed


@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embedArguement = discord.Embed(
            title="**Please specify the amount of messages to delete**!")
        botembedArguement = await ctx.channel.send(embed=embedArguement)
        await asyncio.sleep(1)
        await botembedArguement.delete()
# Kick


@client.command()
@commands.has_permissions(kick_members=True)
async def kick(message, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    embedVar2 = discord.Embed(title="**User kicked!**", color=0x8919cf)
    botembed = await message.channel.send(embed=embedVar2)
    await asyncio.sleep(2)
    await botembed.delete()

# Ban


@client.command()
@commands.has_permissions(ban_members=True)
async def ban(message, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    embedVar3 = discord.Embed(title="**User banned!**", color=0x8919cf)
    botembedvar = await message.channel.send(embed=embedVar3)
    await asyncio.sleep(3)
    await botembedvar.delete()


client.run(KEY)
