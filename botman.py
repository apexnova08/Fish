import os
import discord
import random
import requests
import shutil
from toascii import ImageConverter

import c4
from c4 import c4match

#Private variables - Start

fishi = 338948153627901963
token = "NjM5NjQ2MTkzNTQ2Mjk3MzU0.XbuS8A.IhH1zmfkTWt54ithmCc_qO2xmPs"

#Private variables - End

bot = discord.Client()
prefix = '>'

@bot.event
async def on_ready():
    print ("Logged in as {0.user}".format(bot))
    await bot.change_presence(activity = discord.Activity(type = discord.ActivityType.watching, name = "you"))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if " pp " in message.content or message.content.startswith("pp ") or message.content.endswith(" pp") or message.content == "pp":
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
    if message.content == "nice":
        await message.add_reaction("\U0001f1f3")
        await message.add_reaction("\U0001f1ee")
        await message.add_reaction("\U0001f1e8")
        await message.add_reaction("\U0001f1ea")

    if len(message.attachments) > 0:
        r = requests.get(message.attachments[0], stream = True)
        r.raw.decode_content = True

        with open("local.jpg",'wb') as f:
            shutil.copyfileobj(r.raw, f)
        image = ImageConverter("local.jpg", 0.05, 1.5, "-~+#@").convert()
        if len(image.ascii_image) < 2000:
            await message.channel.send(image.ascii_image)            
        await message.channel.send(str(len(image.ascii_image)) + " characters")
        if os.path.exists("local.jpg"):
            os.remove("local.jpg")

    if message.content.startswith("rand"):
        t = message.content.split()
        a = random.randint(int(t[1]), int(t[2]))
        await message.channel.send(a)

    #Connect Four! - Start

    if message.content.startswith("c4"):
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

    if message.content.startswith("test"):
        e = discord.Embed(description = str(message.author.id) + message.author.mention + " Desc \n test line " + str(message.author) + "\n" + str(message.channel) + "\n" + str(message.channel.guild), color=0xff00ff)
        e.add_field(name = "test name", value = "another text", inline = True)
        e.set_footer(text = "actual bottom text", icon_url = "https://cdn.discordapp.com/attachments/455334275772841984/851906808133451826/Eq0Sh6OUUAMWfv5.jpg")
        await message.channel.send(embed = e)

    if bot.user in message.mentions:
        await message.channel.send("https://pics.me.me/awaken-42160286.png")


bot.run(token)