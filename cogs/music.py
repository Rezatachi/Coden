import discord
from discord.ext import commands
import discord
import random
import asyncio
import youtube_dl
from discord.ext import commands,tasks
from discord.utils import get
from discord import FFmpegPCMAudio
from discord.ext.commands import Bot, has_permissions, CheckFailure
from itertools import cycle
from youtube_dl import YoutubeDL
import os

class music(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Leave
        @client.command()
        async def stop(ctx):
            channel = ctx.message.author.voice.channel
            voice = get(client.voice_clients, guild=ctx.guild)

            if voice and voice.is_connected():
                await voice.disconnect()
                embedLeave = discord.Embed(title=f'**Bot left {channel}**')
                botLeave = await ctx.channel.send(embed=embedLeave)
                await asyncio.sleep(2)
                await botLeave.delete()

            else:
                print("Bot was told to leave voice channel, but was not in one")
                await ctx.send("Don't think I am in a voice channel")
        @client.command()
        async def join(ctx):
         if ctx.author.voice and ctx.author.voice.channel:
                channel = ctx.author.voice.channel
                await channel.connect()        

        # Play
        @client.command()
        async def play(ctx, url: str): 
            def is_connected(ctx):
             voice_client = get(ctx.bot.voice_clients, guild=ctx.guild)
             return voice_client and voice_client.is_connected()
            song_there = os.path.isfile("song.mp3")
            try:
                if song_there:
                    os.remove("song.mp3")
            except PermissionError:
                print("Trying to delete song file, but it's being played")
                await ctx.send("ERROR: Music playing")
                return
            load = await ctx.send("`Getting everything ready now`")
            await asyncio.sleep(2)
            await load.delete()
            if not is_connected(ctx):
                await ctx.send("You are not connected to a voice channel.")   
            voice = get(client.voice_clients, guild=ctx.guild)
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                print("Downloading audio now\n")
                ydl.download([url])

            for file in os.listdir("./"):
                if file.endswith(".mp3"):
                    name = file
                    print(f"Renamed File: {file}\n")
                    os.rename(file, "song.mp3")
            voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: print("Song done!"))
            voice.source = discord.PCMVolumeTransformer(voice.source)
            voice.source.volume = 0.07
            nname = name.rsplit("-", 2)
            await ctx.send(f"Playing: {nname[0]}")
            print("playing\n")
        return

        @client.command(pass_context=True, aliases=['pa', 'pau'])
        async def pause(ctx):

            voice = get(client.voice_clients, guild=ctx.guild)

            if voice and voice.is_playing():
                print("Music paused")
                voice.pause()
                await ctx.send("Music paused")
            else:
                print("Music not playing failed pause")
                await ctx.send("Music not playing failed pause")


        @client.command(pass_context=True, aliases=['r', 'res'])
        async def resume(ctx):

            voice = get(client.voice_clients, guild=ctx.guild)

            if voice and voice.is_paused():
                print("Resumed music")
                voice.resume()
                await ctx.send("Resumed music")
            else:
                print("Music is not paused")
                await ctx.send("Music is not paused")


def setup(client):
    client.add_cog(music(client))