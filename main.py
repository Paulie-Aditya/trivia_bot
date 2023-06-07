'''
If this code interests you, or this has inspired you to create something of your own, do let me know!
I would love to check it out!

'''
import nextcord
from nextcord.ext import commands
import asyncio

import config_triviabot

prefix = "&"
bot = commands.Bot(command_prefix=prefix,intents = nextcord.Intents.all())

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


#All commands can be used only by Paulie and Bot's funder.


#This command is to change the prefix of the bot
@bot.command(name = 'prefix')
async def prefix_command(ctx,arg=prefix):
    if ctx.author.id in [464445762986704918, 457040844105711616]:
        global prefix
        prefix = arg
        bot.command_prefix = prefix
        await ctx.send(f'Prefix of the bot is now `{prefix}`')


    else:
        await ctx.send("You are not authorized to run this command.")

#Command to know balances of the bot.
@bot.command(name = "bals")
async def bals(ctx):
    if ctx.author.id in [464445762986704918, 457040844105711616]:
        await ctx.send("$bals top")
    else:
        await ctx.send("You are not authorized to run this command.")


#Command to make the bot say anything
@bot.command(name = "say")
async def say(ctx,*args):
    if ctx.author.id in [464445762986704918, 457040844105711616]:
        await ctx.send(" ".join([*args]))
    else:
        await ctx.send("You are not authorized to run this command.")


#default values
time_for_trivia = 10    #Time after which triviadrop will start
amt_of_crypto = 0.0     #Amount to giveaway during triviadrop
currency = ""           #Coin/token to giveaway during triviadrop
duration = "1 minute"   #Duration of triviadrop
max_entries = 30        #Max entries of Triviadrop

flag = True             #Flag to setup config and start commands


#Configuration command
#Syntax: {prefix}config [time_for_trivia] [amt_of_crypto] [currency] [duration] [max_entries]
@bot.command(name = 'config')
async def config(ctx,arg1=time_for_trivia,arg2=amt_of_crypto,arg3=currency,arg4=duration,arg5 = max_entries):
    if ctx.author.id in [464445762986704918, 457040844105711616]:
        global time_for_trivia, amt_of_crypto, currency, duration, max_entries,flag,command

        time_for_trivia = arg1
        amt_of_crypto = arg2
        currency = arg3.upper()
        duration = arg4
        max_entries = arg5


        await ctx.send(f'OK! Will do a triviadrop at `{time_for_trivia}` seconds for $`{amt_of_crypto} {currency}` for `{duration}` for `{max_entries}` users')
        command = 'config'
        flag = False

    else:
        await ctx.send("You are not authorized to run this command.")



#To be run in whatever channel you want the trivia drops to happen
#Running this command is mandatory to get the bot started.
#Needs to be run again if config command has been used to change values.
@bot.command(name = "start")

async def trivia(ctx):
    if ctx.author.id in [464445762986704918, 457040844105711616]:
        global flag,amt_of_crypto,currency,duration,max_entries,time_for_trivia,command
        flag = True
        while(flag):
            await ctx.send(f'$triviadrop ${amt_of_crypto} {currency} for {duration} for {max_entries}')
            await asyncio.sleep(time_for_trivia)
        else:
            if command == 'stop':
                await ctx.send(f'`{prefix}start` has been Stopped. Run `{prefix}start`again')
            else:
                await ctx.send(f'Configuration changed. Run `{prefix}start`again')

    else:
        await ctx.send("You are not authorized to run this command.")

#Stop command
@bot.command(name = "stop")
async def stop(ctx):
    if ctx.author.id in [464445762986704918, 457040844105711616]:
        global flag,command
        await ctx.send(f'Stopping the `{prefix}start` command')
        command = 'stop'
        flag = False


    else:
        await ctx.send("You are not authorized to run this command.")


#Help Command
@bot.command(name = "helpme")
async def helpme(ctx):
    if ctx.author.id in [464445762986704918, 457040844105711616]:

        embed=nextcord.Embed(title = "My commands", color= 0x21f9fd)
        embed.add_field(name = f'`{prefix}config`', value  = f'How to Use: `{prefix}config [time_for_trivia] [amt_of_crypto] [currency] [duration] [max_entries]`\n\n\n`[time_for_trivia]` -> Time after which triviadrop will be scheduled\n`[amt_of_crypto]` -> Amount to giveaway during triviadrop\n`[currency]` -> Coin/token to giveaway during triviadrop\n`[duration]` -> Duration of triviadrop\n`[max_entries]` -> Max entries of Triviadrop',inline=False)
        embed.add_field(name = f'`{prefix}start`' , value = 'Run this command in whichever channel you want to have the Trivia Drops in.\nRunning this command is mandatory to get the bot started.\nNeeds to be run again if config command has been used.',inline=False)
        embed.add_field(name = f'{prefix}prefix', value = f'Syntax: `{prefix}prefix [new_prefix]`\nSets a new prefix for the bot.')
        embed.add_field(name = f'`{prefix}helpme`', value = 'This is what got you here.',inline=False)
        embed.add_field(name = f'`{prefix}bals`', value ='This shows my balances.',inline=False)
        embed.add_field(name = f'`{prefix}say`', value = 'Makes me say whatever you want me to.',inline=False)

        await ctx.send(embed=embed)
        pass
    else:
        await ctx.send("You are not authorized to run this command.")


bot.run(config.trivia_bot_token)