import discord
from discord.ext import tasks, commands
import logging
import os
import random
import eve
import web
import requests
import funcsnfish as ff

import c4
from c4 import c4match

token = os.getenv("DISCORD_TOKEN")
master = int(os.getenv("MASTER"))

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

prefix = '>'
bot = commands.Bot(command_prefix=prefix, intents=intents)


# VARS #
URL = "https://fish-8v65.onrender.com/"
structstates = {}

@bot.event
async def on_ready():
    global masterUser
    masterUser = await bot.fetch_user(master)
    await masterUser.send("https://cdn.discordapp.com/attachments/1379858761417494560/1497956290394062978/awake-woke.gif?ex=69ef6802&is=69ee1682&hm=a913f9234c5993185ecfb9404fcbb5023a344004edc365adaec5ecb46e777f64")
    if not keepAwake.is_running():
        keepAwake.start()
    if not monitorStructures.is_running():
        monitorStructures.start()

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    # -------------------
    # MASTER - STARTE
    # -------------------
    if message.author.id == master:
        if message.content.lower() == "test":
            structPingChannel = message.channel
            await structPingChannel.send(type(structPingChannel))

        if message.content.lower() == "dm1":
            await message.author.send("test message")
        if message.content.lower() == "dm2":
            await masterUser.send("test message")

        if message.content.lower() == (f"{prefix}evelogin"):
            await message.channel.send(eve.make_auth_url(message.author.id))

        if message.content.lower() == (f"{prefix}info"):
            await message.channel.send(eve.get_character_info("2123045230", message.author.id))

        if message.content.lower() == (f"{prefix}verify"):
            await message.channel.send(eve.verify_token(message.author.id))

    # -------------------
    # STRUCTURE PINGS
    # -------------------
    if message.content.startswith(f"{prefix}structurepings"):
        s = message.content.split()
        if message.content == (f"{prefix}structurepings") or s[1] == "auth":
            await message.channel.send(f"Log in your holding character [HERE]({eve.makeAuthUrl(message.author.id, message.channel.id)})")


    global structstates
    if message.content.lower() == (f"{prefix}structs"):
        structsdict = eve.get_corp_structures(message.author.id)
        for s in structsdict:
            ping = False
            embedColor = 0x009900
            sid = str(s["structure_id"])
            
            embedContent = s["state"]
            oldstate = structstates.get(sid)
            if oldstate and oldstate != s["state"]: ping = True
            if s["state"] != "shield_vulnerable": embedColor = 0x990000
            structstates[s["structure_id"]] = s["state"]

            fuelleft, fueldays = eve.time_remaining(s['fuel_expires'])
            if fueldays < 7:
                ping = True
                embedColor = 0x990000
            embedContent = embedContent + "\n\n" + f"Fuel: {fuelleft}"
            if ping: embedContent = embedContent + "\natPING"
            e = discord.Embed(title = s["name"], description = embedContent, color = embedColor)
            e.set_thumbnail(url = f"https://images.evetech.net/types/{s['type_id']}/render?size=64")
            await message.channel.send(embed = e)
        print(structsdict)

    if ff.wordInString("pp", message.content.lower()):
        a = random.randint(1, 2)
        if a == 2:
            await message.add_reaction("\U0001f1f8")
            await message.add_reaction("\U0001f1f2")
            await message.add_reaction("\U0001f1f4")
            await message.add_reaction("\U0001f1f1")
        else:
            await message.add_reaction("\U0001f1e7")
            await message.add_reaction("\U0001f1ee")
            await message.add_reaction("\U0001f1ec")
    if ff.wordInString("nice", message.content.lower()) or ff.wordInString("69", message.content.lower()):
        await message.add_reaction("\U0001f1f3")
        await message.add_reaction("\U0001f1ee")
        await message.add_reaction("\U0001f1e8")
        await message.add_reaction("\U0001f1ea")

    #Connect Four! - Start

    if message.content.startswith("c4 "):
        s = message.content.split()
        match = None
        if s[1] == "play" and len(message.mentions) == 1 and message.mentions[0] != message.author and message.mentions[0] != bot.user:
            chckp = c4.checkPlayers(message.author, message.mentions[0])
            if chckp is None:
                match = c4match.play(message.author, message.mentions[0], message.channel)
            else:
                match = c4.getMatch(chckp)
                embedContent = chckp.mention + " currently has an active Connect Four match!\nSettle the active match first or abandon it by typing " + prefix + "*c4 leave*\n"
                
                e = discord.Embed(title = "", description = embedContent, color=0x009999)
                await message.channel.send(embed = e)
                match = None

        elif s[1] == "leave":
            match = c4.getMatch(message.author)
            if match is not None:
                embedContent = "**Match details**\nPlayer 1: " + str(match.player1) + "\nPlayer 2: " + str(match.player2)
                embedContent = embedContent + "\nServer: " + str(match.channel.guild)
                embedContent = embedContent + "\nChannel: #" + str(match.channel)
                
                e = discord.Embed(title = "Match Removed", description = embedContent, color=0xff5050)
                await message.channel.send(embed = e)
                c4.clearMatch(match)
                match = None

        elif s[1].isnumeric() == True:
            if int(s[1]) <= 7 and int(s[1]) > 0:
                match = c4.getMatch(message.author)
                if match is not None and match.channel == message.channel:
                    match = c4match.turn(match, message.author, int(s[1]))
                else:
                    match = None
        
        if match is not None:
            embedContent = match.player1.mention + " :red_circle: vs. :blue_circle: " + match.player2.mention
            embedContent = embedContent + "\n\n" + match.displayBoard()
            embedColor = 0x009999
            if match.status == "Concluded":
                embedContent = embedContent + "\n" + "Concluded: " + message.author.mention + " Wins! :tada:"
                embedColor = 0x00cc66
                c4.clearMatch(match)
            elif match.status == "Stalemate":
                embedContent = embedContent + "\n" + "Concluded: " + "Stalemate :moyai:"
                embedColor = 0x999999
                c4.clearMatch(match)
            else:
                embedContent = embedContent + "\n" + "Turn: " + match.turn.mention
            e = discord.Embed(title = match.title, description = embedContent, color = embedColor)
            e.set_thumbnail(url = "https://cdn.discordapp.com/attachments/455334275772841984/850489873550278676/greet.gif")
            await message.channel.send(embed = e)

    #Connect Four! - End
    
    await bot.process_commands(message)

@tasks.loop(minutes=10)
async def keepAwake():
    try:
        r = requests.get(URL)
        print("Ping status:", r.status_code)
    except Exception as e:
        print("Ping failed:", e)

@tasks.loop(minutes=2)
async def monitorStructures():
    try:
        profiles = ff.getAllProfiles()
        await masterUser.send(profiles)
        if not profiles: return
        for p in profiles:
            channel = bot.get_channel(profiles[p]["channel"])

            # DELETE ALL MESSAGES IN CHANNEL
            async for msg in channel.history(limit=None):
                await msg.delete()

            structures = eve.get_corp_structures(p)
            for s in structures:
                embedColor = ff.colors["green"]
                embedContent = s["state"]

                fuelleft, fueldays = eve.time_remaining(s['fuel_expires'])
                embedContent = embedContent + "\n\n" + f"Fuel: {fuelleft}"
                e = discord.Embed(title = s["name"], description = embedContent, color = embedColor)
                e.set_thumbnail(url = f"https://images.evetech.net/types/{s['type_id']}/render?size=64")
                await channel.send(embed = e)

    except Exception as e:
        await masterUser.send(f"structurepings failure: {e}")
        return

@bot.command()
async def test(ctx):
    await ctx.send("sex?")

web.keep_alive()
bot.run(token, log_handler=handler, log_level=logging.DEBUG)