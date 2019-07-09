import discord
from discord.ext.commands import Bot
from discord.ext import commands
from discord.voice_client import VoiceClient
import sqlite3 as sqlite
import asyncio
import sys
import os
import json
import random

#LICENSE KEY, DO NOT CHANGE!
LICENSE = "ALPHA"

#QUICK SETTINGS, SEE CONFIG FOR EXPLANATIONS!
TOKEN = "EMPTY"
STATUS = "Scrims.pro"
PREFIX = "!"
ANNOUNCEMENT_CHANNEL = "551586236280602644"
UPDATE_CHANNEL = "551586346158915585"

#Permissions: 
ADMIN_ROLEID_1 = "551588898594357248" #Get the ROLE id for any role you want to be able to use !admin commands
ADMIN_ROLEID_2 = "535214528531529758" #Get the ROLE id for any role you want to be able to use !admin commands
ADMIN_ROLEID_3 = "508724522610982923" #Get the ROLE id for any role you want to be able to use !admin commands
ADMIN_ROLEID_4 = "508723361979826192" #Get the ROLE id for any role you want to be able to use !admin commands
ADMIN_ROLEID_5 = "509712095651299339" #Get the ROLE id for any role you want to be able to use !admin commands

#other settings/placeholders
WEBSITE = "https://scrims.pro" #Sets our website link for our !website command
TEAMSPEAK = "https://discord.gg/PTRb2BT" #Sets our TS link for !ts
BROADCAST_CHANNEL = "551586236280602644" #Sets channel bot will message when you use !admin broadcast {message}
UPDATE_CHANEL = "551586346158915585"
PARTICIPATION_CHANNEL = "551609100753174539"

Client = discord.Client()
client = commands.Bot(command_prefix="!")  #Doesn't do anything, when I used a onMessage even not onCommand, may update if I find it makes a difference

LOGINPUTS = False
dict = {}
codes = []
REQ = 0
names = []

gamesEmbed = discord.Embed(
    title = "Current Games: ",
    description = "",
    color = discord.Color.green()
    )

@client.event
async def on_ready():
    global QUEUE
    print("Scrims Pro Bot has been Initiailized. Made by PickleZ#8019") #On-Load message, please leave my name in here.
    print(" ")
    await client.change_presence(game=discord.Game(name=STATUS)) #Changes the bot's 'playing' game. Set this in settings on line 13
    


@client.event
async def on_message(message): #I use the onMessage event to basically track commands. May change to onCommand if I find it is better
    global LOGINPUTS
    global PREFIX
    global REQ
    global INPUTLOG
    global dict
    global codes
    global names
    server = message.server
    
    if len(message.content) == 3 and str(message.channel) == "queue" and LOGINPUTS == True:
        print("Message has been logged: " + str(message.content))
        await client.delete_message(message)
        if message.content.upper() == "REQ":
            REQ = REQ + 1
        else:
            name = str(message.author)
            code = str(message.content).upper()
            
            if len(names) == 0:
                print("Bypassing")
            
            inList = False
            
            for NAME in names:
                if NAME == name:
                    print("Duplicate found")
                    
                    inList = True
            
            if inList == False:
                if len(codes) == 0:
                  codes.append(code)
                  names.append(name)
                  await client.send_message(message.author, "You have added the code: " + str(message.content).upper() + " to the queue's team list.")
                else:
                  for CODE in codes.copy():
                    if CODE == code:
                     print("Bypassing")
                    else:
                     codes.append(code)
                     names.append(name)
                     await client.send_message(message.author, "You have added the code: " + str(message.content).upper() + " to the queue's team list.")
     
                if len(dict) == 0:
                  dict[str(code)] = str(name)
        
                else:
                  for CODE in dict.copy():
                   if code == CODE:
                    dict[CODE] = str(dict[CODE]) + "\n" + str(name)
                   else:
                    dict[code] = str(name)
            
            else:
                await client.send_message(message.author, "Sorry, but you have already entered a code for this queue, unfortunately if you made a mistake it isn't possible to change your code at this time.")
  
  
        
    if len(message.content) != 3 and str(message.channel) == "queue" and LOGINPUTS == True and str(message.author) != "ScrimsPro#2086":
        print("Message has not been logged and has been deleted.")
        await client.send_message(message.author, "You have entered an invalid server code, make sure it is 3 digits long and please try again!")
        await client.delete_message(message)
        
    
    
    if message.content.upper() == str(PREFIX) + "WEBSITE" or message.content.upper() == str(PREFIX) + "TWITTER" or message.content.upper() == str(PREFIX) + "TWEET":
        await client.send_message(message.channel, "Our Website Link is: " + str(WEBSITE))
    
    elif message.content.upper() == str(PREFIX) + "EMAIL":
        await client.send_message(message.channel, "You can email us about **Business** concerns at: scrimspro.bot@gmail.com. _Note: Any non-business concerns can be done in DM's!")
  
    #Returns the teamspeak URL(if that's what you call it) to the user
    elif message.content.upper() == str(PREFIX) + "DISCORD" or message.content.upper() == str(PREFIX) + "TEAMSPEAK" or message.content.upper() == str(PREFIX) + "VOICE":
        await client.send_message(message.channel, "Our discord invite link is: " + str(TEAMSPEAK))
 
   #Admin only command: Broadcasts 
    elif message.content.upper().startswith(str(PREFIX) + "ADMIN BROADCAST"):
        args = message.content.split(" ")
        server = message.server
        if await permissionCheck(message) == True:
            await client.send_message(server.get_channel(str(BROADCAST_CHANNEL)), "{0}".format(" ".join(args[2:])))
        else:
            await client.send_message(message.channel, "You don't have permission to use that admin command. You must be Moderator or higher.")
    
    elif message.content.upper().startswith(str(PREFIX) + "ADMIN PUSH"):
        args = message.content.split(" ")
        server = message.server
        if await permissionCheck(message) == True:
            await client.send_message(server.get_channel(str(UPDATE_CHANEL)), "**Update:** {0}".format(" ".join(args[2:])))
        else:
            await client.send_message(message.channel, "You don't have permission to use that admin command. You must be a Moderator or higher.")
            
    elif message.content.upper().startswith(str(PREFIX) + "TICKET"):
       server = message.server
       author = message.author
       args = message.content.split(" ")
       everyone = discord.PermissionOverwrite(read_messages=False)
       mine = discord.PermissionOverwrite(read_messages=True)
       
       ticketChannel = await client.create_channel(server, str(args[1]), (server.default_role, everyone), (author, mine))
       
       string = ""
       
       for word in args:
           if word == args[0] or word == args[1]:
               print("Bypassing, don't mind me :)")
           else:
               string = string + str(word) + " "
       
       await newTicketEmbed(ticketChannel, string)
       
    elif message.content.upper().startswith(str(PREFIX) + "ADMIN MARK"):
        if await permissionCheck(message) == True:
            args = message.content.split(" ")
            
            markage = str(args[2])
            
            originalName = str(message.channel.name)
            
            print(originalName[0:2])
            
            if str(originalName[0:2]) == "p-" or str(originalName[0:2]) == "w-" or str(originalName[0:2]) == "r-":
                originalName = originalName[2:]
        
            if markage.upper() == "PENDING":
                await client.edit_channel(message.channel, name = "p-" + str(originalName))
                pinMe = await client.send_message(message.channel, "I have marked this channel: **PENDING**")
                await client.pin_message(pinMe)
                
            elif markage.upper() == "WAITING":
                await client.edit_channel(message.channel, name = "w-" + str(originalName))
                pinMe = await client.send_message(message.channel, "I have marked this channel: **WAITING**")
                await client.pin_message(pinMe)
                
            elif markage.upper() == "RESOLVED":
                await client.edit_channel(message.channel, name = "r-" + str(originalName))
                
    
    elif message.content.upper().startswith(str(PREFIX) + "PARTICIPATION CHECK"):
        
        args = message.content.split(" ")
        
        types = str(args[2])
        goal = str(args[3])
        
        if await permissionCheck(message) == False:
            await client.send_message(message.channel, "Hey! You can't use that command, you don't have the correct permissions!")
            
        else:
            await startParticipationCheck(message, types, goal)
            
            
    elif message.content.upper().startswith(str(PREFIX) + "TEAM CREATE"):
        await startTeamCreation(message)
            
                
    elif message.content.upper().startswith(str(PREFIX) + "ADMIN PREFIX"):
        args = message.content.split(" ")
        
        newPrefix = str(args[2])
        
        PREFIX = newPrefix
        
        await client.send_message(message.channel, "I have changed the prefix to be: '" + str(newPrefix) + "'!")
        
    elif message.content.upper().startswith(str(PREFIX) + "QUEUE START"):
        gamesEmbed = discord.Embed(
            title = "Current games:",
            description = "",
            color = discord.Color.red()
            )
            
        args = message.content.split(" ")
        
        type = str(args[2])
        countdown = str(args[3])
        
        description = ""
        
        eyo = args[4:]
        
        for word in eyo:
            description = description + word + " "
        
        await startQueue(message, type, countdown, description)
        
    elif message.content.upper().startswith(str(PREFIX) + "ADMIN STATUS"):
        args = message.content.split(" ")
        
        string = ""
        for word in args[2:]:
            string = string + word + " "
        
        await client.change_presence(game=discord.Game(name=str(string)))
        await client.send_message(message.channel, "I have changed my playing status to be: '" + str(string) + "'!")
        
       
    elif message.content.upper().startswith(str(PREFIX) + "ADMIN CLOSE"):
        if await permissionCheck(message) == True:
            await closeChannel(message.channel, message.author, message.server)
        else:
            await client.send_message(message.channel, "Sorry, but you need to have an administrative role to do that!")
       
    #Admin only command: Brings up help menu about our admin commands 
    elif message.content.upper().startswith(str(PREFIX) + "ADMIN") or message.content.upper().startswith(str(PREFIX) + "ADMIN HELP") or message.content.upper().startswith(str(PREFIX) + "ADMINS"):
        if await permissionCheck(message) == True:
            await adminHelp(message.channel)
        else:
            await client.send_message(message.channel, "You don't have permission to use that admin command. You must be a Moderator or higher.")

    elif message.content.upper().startswith(str(PREFIX) + "HELP") or message.content.upper().startswith(str(PREFIX) + "COMMANDS"):
        await sendHelpEmbed(message.channel)
    




@client.event
async def on_reaction_add(reaction, user):
    print(str(reaction.emoji))
    if str(reaction.emoji) == "<:csgo:544232345620709376>":
        role = discord.utils.get(user.server.roles, name="CS:GO")
        await client.add_roles(user, role)
        print("Added role CS:GO to user: " + str(user))
    

async def startQueue(message, type, countdown, description):
    global LOGINPUTS
    global codes
    global dict
    global REQ
    dict = {}
    codes = []
    server = message.server
    sendChannel = server.get_channel(str("551624070865747978"))
    
    embed = discord.Embed(
        title = "Queue Beginning",
        description = "",
        color = discord.Color.green()
    )
    embed.set_footer(text="Bot made by: PickleZ#8019")
    embed.add_field(name = "Type: ", value = str(type))
    embed.add_field(name = "Countdown: ", value = str(countdown))
    embed.add_field(name = "Description: ", value = str(description), inline=False)
    
    queueMSG = await client.send_message(sendChannel, embed=embed)
    editMe = await client.send_message(sendChannel, "@everyone")
    
    temp = 0
    counter = int(countdown)
    
    while counter != 0:
        counter = counter - 1
        embed = discord.Embed(
            title = "Queue Beginning",
            description = "",
            color = discord.Color.green()
        )
        embed.set_footer(text="Bot made by: PickleZ#8019")
        embed.add_field(name = "Type: ", value = str(type))
        embed.add_field(name = "Countdown: ", value = str(counter))
        embed.add_field(name = "Description: ", value = str(description), inline=False)
        
        
        queueMSG = await client.edit_message(queueMSG, embed=embed)
        if counter <= 5:
            editMe = await client.edit_message(editMe, "@everyone | " + str(counter) + " seconds remain")
        await asyncio.sleep(1)
            
    
    await client.delete_message(queueMSG)
    info = await client.send_message(sendChannel, "The queue has begun! Every ready up! @everyone\n\n**Instructions:**\nOnce you join a game, take the last 3 digits of your server's code (top left corner), and then type it in this channel. This channel will be unlocking in 5 seconds.\n\nNeed more help? Use the !queue help command to learn more about how our queue system works!")
    await client.delete_message(editMe)
    
    
    lockedPermissions = discord.PermissionOverwrite(read_messages=True, send_messages=False)
    unlockedPermissions = discord.PermissionOverwrite(read_messages=True, send_messages=True)
    
    await client.edit_channel_permissions(sendChannel, server.default_role, unlockedPermissions)
    
    changeAble = await client.send_message(sendChannel, "I have unlocked this channel for 30 seconds")

    counterDowner = 30
    LOGINPUTS = True
    
    while counterDowner != 0:
        await asyncio.sleep(1)
        changeAble = await client.edit_message(changeAble, "I have unlocked this channel for " + str(counterDowner) + " seconds")
        counterDowner = counterDowner - 1
    
    await client.edit_channel_permissions(sendChannel, server.default_role, lockedPermissions)
    await client.delete_message(changeAble)
    await client.delete_message(info)
    
    await client.send_message(sendChannel, "One second, refreshing list of players...")
    
    await asyncio.sleep(3)
    
    sendEmbed = discord.Embed(
        title = "Current Games: ",
        description = "",
        color = discord.Color.blue()
    )
    
    for CODE in codes:
        names = str(dict[CODE])
        sendEmbed.add_field(name=str(CODE), value=str(names))
    
    sendEmbed.set_footer(text="Requeue requests: " + str(REQ))
    
    done = await client.send_message(sendChannel, embed=sendEmbed)
        
    
    
        
        
        
        
    
                
async def startTeamCreation(message):
    server = message.server
    user = str(message.author)
    
    await client.send_message(message.author, "You have initiated the team creation wizard. To begin, please type in the desired name for your team.")
    name = client.wait_for_message(channel = message.author)
    args = name.content.split()
    while len(name.content) <= 3 or len(args) >= 2:
        await client.send_message(message.author, "Sorry, but your name is either too short, or have too many arguments (only one word allowed, please retype it.")
        name = client.wait_for_message(channel = message.author)
    
    await client.send_message("Success! Now for your team, do you want a voice channel, text channel, or both.\n\nRespond with:\n**A** - To signify just a voice channel\n**B** - To signify just a text channel\nor **C** - T signify both a text and voice channel")
    type = client.wait_for_message(channel = message.author)
    
    if type.content.upper() == "A":
        await client.send_message(message.author, "Creating just a voice channel for you... done!")
        everyone = discord.PermissionOverwrite(view_channel=False, connect=False)
        mine = discord.PermissionOverwrite(view_channel=True, connect=True)
        tempVoice = await client.create_channel(server, str(name), (server.default_role, everyone), (message.author, mine), type=discord.ChannelType.voice)
    elif type.content.upper() == "B":
        await client.send_message(message.author, "Creating just a text channel for you... done!")
        everyone = discord.PermissionOverwrite(read_messages=False)
        mine= discord.PermissionOverwrite(read_messages=True)
        tempText = await client.create_channel(server, str(name), (server.default_role, everyone), (message.author, mine))
        await client.send_message(tempText, "Channel created!")
    elif type.content.upper() == "C":
        await client.send_message(message.author, "Creating both a text, and voice channel for you... done!")
        everyone = discord.PermissionOverwrite(read_messages=False)
        mine= discord.PermissionOverwrite(read_messages=True)
        tempText = await client.create_channel(server, str(name), (server.default_role, everyone), (message.author, mine))
        await client.send_message(tempText, "Channel created!")
        everyoneVoice = discord.PermissionOverwrite(view_channel=False, connect=False)
        mineVoice = discord.PermissionOverwrite(view_channel=True, connect=True)
        tempVoice = await client.create_channel(server, str(name), (server.default_role, everyoneVoice), (message.author, mineVoice), type=discord.ChannelType.voice)
    

async def startParticipationCheck(message, types, goal):
    server = message.server
    CHANNEL = server.get_channel(str(PARTICIPATION_CHANNEL))
    embed = discord.Embed(
        title = "",
        description = "React with a checkmark to join the queue",
        color = discord.Color.blue()
    )
    embed.add_field(name="Type:", value=str(types))
    embed.add_field(name="Goal:", value=str(goal))
    embed.set_footer(text="Checked by " + str(message.author))
    embed.set_author(name="Participation Check!")
    
    participationMessage = await client.send_message(CHANNEL, embed=embed)
    await client.add_reaction(participationMessage, "✅")
    await asyncio.sleep(1)
    
    participants = 0
    while participants != int(goal):
        await client.wait_for_reaction("✅", message=participationMessage)
        participants = participants + 1
    
    await client.send_message(CHANNEL, "We have reached the goal of: **" + str(goal) + "**! The Queue will start shortly!")
    await asyncio.sleep(5)
    await client.delete_message(participationMessage)
    


async def adminHelp(channel): #Function to send the admin embed link
    embed = discord.Embed(
        title = '!admin ban [player]',
        description = 'Permenantly bans a player',
        colour = discord.Color.blue()
    )
    embed.set_footer(text='bot by: PickleZ#8019')
    embed.set_author(name='Scrims.Pro Bot v1.1')
    embed.add_field(name='!admin broadcast [message]', value='Announces your message to the #announcements channel', inline=False)
    embed.add_field(name='!admin push [message]', value='Pushes an update, announces in the #updates channel', inline=False)
    embed.add_field(name='!admin close', value='Closes the channel that you are in.', inline=False)
    embed.add_field(name='!admin mark [status]', value='Sets ticket as PENDING, WAITING, or RESOLVED', inline=False)
    embed.add_field(name='!admin prefix [newPrefix]', value='Sets the new bot prefix, only temporary', inline=False)
    embed.add_field(name='!admin blacklist [@User]', value='Blacklists a particular user from using the queue system OR ticket system', inline=False)
    embed.add_field(name='!admin status [newStatus]', value='Changes the bots status to [newStatus]', inline=False)
    
    await client.send_message(channel, embed=embed)

        
async def sendHelpEmbed(channel): #Function to send the help embed link
    embed = discord.Embed(
        title = 'Help Commands: ',
        description = " ",
        colour = discord.Color.blue()
    )
    embed.set_footer(text="bot by: PickleZ#8019")
    embed.set_author(name="Scrims.Pro Bot")
    embed.add_field(name="!help", value ="Brings up this GUI, shows all user commands", inline=False)
    embed.add_field(name="!time", value="Shows time until the next queue begins", inline=False)
    embed.add_field(name="!team", value="Begins the creation of a team", inline=False)
    embed.add_field(name="!ticket [Reason]", value="Creates a ticket with [reason]", inline=False)
    
    await client.send_message(channel, embed=embed)

async def newTicketEmbed(channel, description): #Function to send the help embed link
    embed = discord.Embed(
        title = 'Description: ',
        description = "\n" + str(description),
        colour = discord.Color.blue()
    )
    embed.set_footer(text="bot by: PickleZ#8019")
    embed.set_author(name="Ticket Created!")
    
    await client.send_message(channel, embed=embed)

async def closeChannel(channel, author, server):
    
    waitFor = await client.send_message(channel, "Are you sure you want to close this channel? React with a ✅if you want to continue with the closing of this ticket.")
    
    await client.add_reaction(waitFor, "✅")
    await asyncio.sleep(1)
    await client.wait_for_reaction("✅", message=waitFor)
    
    
    time = 60
    
    embed = discord.Embed(
        title = 'Ticket Closing in: ',
        description = "\n" + str(time) + " seconds",
        colour = discord.Color.blue()
    )
    embed.set_footer(text="Closed By: " + str(author))
    
    initialEmbed = await client.send_message(channel, embed=embed)
    
    while time != 0:
        await asyncio.sleep(1)
        time = time - 1
        embed = discord.Embed(
            title = 'Ticket Closing in: ',
            description = "\n" + str(time) + " seconds",
            colour = discord.Color.blue()
        )
        embed.set_footer(text="Closed By: " + str(author))
        
        initialEmbed = await client.edit_message(initialEmbed, embed=embed)
        
    await client.delete_channel(channel)
    

async def permissionCheck(message): #Permission check system for all roles defined in settings
    if ADMIN_ROLEID_1 in [role.id for role in message.author.roles]:
        return True
    elif ADMIN_ROLEID_2 in [role.id for role in message.author.roles]:
        return True
    elif ADMIN_ROLEID_3 in [role.id for role in message.author.roles]:
        return True
    elif ADMIN_ROLEID_4 in [role.id for role in message.author.roles]:
        return True
    elif ADMIN_ROLEID_5 in [role.id for role in message.author.roles]:
        return True
    
client.run(TOKEN)
