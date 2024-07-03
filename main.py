import time
import discord
from discord.ext import tasks
import os
from dotenv import load_dotenv
from mcstatus import JavaServer

load_dotenv()
TOKEN = os.getenv('TOKEN')
VOICE1 = int(os.getenv('VOICE1_ID'))
VOICE2 = int(os.getenv('VOICE2_ID'))

intents = discord.Intents.default()
intents.guilds = True
bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}') 
    check_server_status.start() 

async def update_status(status, plrcount):
    guild = discord.utils.get(bot.guilds)
    if guild is None:
        print("Did not found guild")
        return
    statusChannel = guild.get_channel(VOICE1)
    plrChannel = guild.get_channel(VOICE2)
    if statusChannel and isinstance(statusChannel, discord.VoiceChannel):
        try:
            newChannelText = str(status)
            if statusChannel.name != newChannelText:  
                await statusChannel.edit(name=newChannelText)
                print(f'Status Channel renamed to {newChannelText}')
        except discord.Forbidden:
            print("Permission Error on status channel")
        except discord.HTTPException as e:
            print(f"HTTP Exception: {e}")

    if plrChannel and isinstance(plrChannel, discord.VoiceChannel):
        try:
            newPlayerChannelText = str(plrcount)
            if plrChannel.name != newPlayerChannelText: 
                await plrChannel.edit(name=newPlayerChannelText)
                print(f'Player Channel renamed to {newPlayerChannelText}')
        except discord.Forbidden:
            print("Permission Error on player channel")
        except discord.HTTPException as e:
            print(f"HTTP Exception: {e}")

@tasks.loop(minutes=1)
async def check_server_status():
    serverOnlineStatus = "Status: Offline"
    serverPlayerCount = 0
    try:
        server = JavaServer.lookup("hellenicraft.mine.nu:25565")
        status = server.status()
        serverOnlineStatus = "Status: Online"
        serverPlayerCount = f"Players: {status.players.online}/16"
    except Exception as e:
        serverOnlineStatus = "Status: Offline"
        serverPlayerCount = 0
    print(f"Server Status: {serverOnlineStatus}")
    print(f"Player Count: {serverPlayerCount}")
    await update_status(serverOnlineStatus, serverPlayerCount)

bot.run(TOKEN)
