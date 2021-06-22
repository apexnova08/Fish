import os
import discord
import random
from mosquitoman import ping

import c4
from c4 import c4match

#Private variables - Start

#fishi
#token

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
                embedContent = chckp.mention + " currently has an active Connect Four match!\nSettle the active match first or abandon it by typing *" + prefix + "c4 leave*\n"
                
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
        e = discord.Embed(description = message.author.mention + "Desc \n test line", color=0xff00ff)
        e.add_field(name = "test name", value = "another text", inline = True)
        await message.channel.send(embed = e)

    if message.content == bot.user.mention:
        await message.channel.send("https://pics.me.me/awaken-42160286.png")

ping()
bot.run(os.environ['discToken'])