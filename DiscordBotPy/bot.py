import os

import discord
import asyncio

from youtube_dl import YoutubeDL
from discord.ext import commands
from dotenv import load_dotenv

file_name = "tiempo.txt"

def get_time():
    file = open(file_name, "r")
    time = int(file.read())
    file.close()
    return time

def set_time(time):
    file = open(file_name, "w")
    file.write(str(time))
    file.close()

load_dotenv()
TOKEN = os.getenv('TOKEN')
bot = commands.Bot(command_prefix="t")

def is_connected(ctx):
    voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
    return voice_client and voice_client.is_connected()

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected')

@bot.command(name="roleado", pass_context=True, help="Trolea a una persona reproduciendo el baile del troleo")
async def nene_malo(ctx):
    vox = ctx.author.voice
    ydl_opts = {'format': 'bestaudio', 'noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'} 
    if(not (vox and vox.channel)):
        await ctx.send("Conéctate primero a un canal para trolear")
    else:
        if(not is_connected(ctx)):
            await vox.channel.connect()
            voice = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
            i = get_time()
            i+=1
            set_time(i)
            print(i)
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info("https://www.youtube.com/watch?v=qe5-ywmuKOg", download=False)
            URL = info['formats'][0]['url']
            voice.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
            voice.is_playing()
            await asyncio.sleep(15)
            voice.stop()
            await voice.disconnect()
        elif(is_connected(ctx) and vox.channel == ctx.voice_client.channel):
            await ctx.send("Ya estoy troleado al que me dijiste")
        else:
            await ctx.send("Ya estoy troleando a alguien más")

@bot.command(name="opo", pass_context=True, help="Desconecta al bot mientras reproduce el audio")
@commands.has_role('Admin')
async def adios(ctx):
    vox = ctx.author.voice
    if(vox and vox.channel and is_connected and vox.channel == ctx.voice_client.channel):
        voice = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        await voice.disconnect()

@bot.command(name="iempo", pass_context=True, help="Muestra cuanto tiempo se ha usado el bot para trolear gente de manera exitosa")
async def tiempo(ctx):
    await ctx.send("He gastado {0} minutos troleando gente".format(round(get_time()*0.25, 1)))
bot.run(TOKEN)

