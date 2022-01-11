
import os
import random
import discord
import asyncio
import requests
import feedparser
import datetime
import re
from coinpaprika import client as Coinpaprika
from tabulate import tabulate
from decimal import Decimal
import sched, time
from discord.ext import tasks, commands
from discord.ext.commands import CommandNotFound
import re
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from discord.ext import commands
from dotenv import load_dotenv
import json

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
print('(XRPHolder) Loaded.')


xbot = commands.Bot(command_prefix='*')
xbot.remove_command("help")

cp = Coinpaprika.Client()


@xbot.event
async def on_message(message):
	if message.author == xbot.user:
		return
	if message.content.lower().startswith('*'):
		cmdChannel = COMMAND_CHANNEL_ID_HERE
		if(message.channel.id == cmdChannel):
			await message.channel.trigger_typing()
			await xbot.process_commands(message)
		else:
            #command attempted in non command channel - redirect user
			await message.channel.send('Write this command in <#' + str(cmdChannel) + '>', delete_after=10)

@xbot.event
async def on_ready():
	guild = xbot.get_guild(GUILD_ID_HERE)
	me = guild.me
	print('---')
	print(xbot.user.name)
	print(xbot.user.id)
	print('---')
	print('(XRPHolder) Ready.')
	await xbot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="XRP Charts Rise"))
	print('(XRPHolder) Set Status')
	await me.edit(nick="XRPHolder")
	print('(XRPHolder) Set Nickname')



@xbot.command(name='help', help='command list/help')
async def help(ctx):
	print("(XRPHolder) Help Command Ran By " + ctx.author.nick)
	await ctx.send("Use the *clp command to start XRP live price")

global count
count = 0;

@tasks.loop(seconds=15)
async def called_once_everybit(arg):
	global count
	guild = xbot.get_guild(GUILD_ID_HERE)
	me = guild.me
	FOURPLACES = Decimal(100) ** -2
	coin = requests.get('https://cex.io/api/last_price/' + str(arg.upper()) + "/" + "USD").json()
	coinname = coin['curr1']
	price = coin['lprice']
	count += 1
	currentn = me.display_name
	currentp = re.sub('[$]','',currentn)
	updatingp = str(price)
	comparep = re.sub('[$]','',updatingp)
	print("(LivePriceUpdater)(Status Change) Checking Prices...")
	print("(LivePriceUpdater)(Status Change) Old Price: $" + str(currentp) + " | Updating Price: $" + str(comparep))
	if(currentp != comparep):
		print("(LivePriceUpdater) " + str(count) + " " + str(coinname) + " $" + str(price))
		print("(LivePriceUpdater)(Status Change) Price Update Detected! Updating Status")
		await me.edit(nick="$" + str(price))
		await xbot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name= str(coinname) + " USD"))
	else:
		print("(LivePriceUpdater) " + str(count) + " " + str(coinname) + " $" + str(price))
		print("(LivePriceUpdater)(Status Change) Price hasn't changed.")

	#guild = arg.message.guild.id


@xbot.command(name='clp', help='sets bots description to live updating XRP price(CRYPTO ONLY)')
async def updatingprice(ctx):
	print("(XRPHolder) Crypto Live Updating Price Activated")
	guild = xbot.get_guild(GUILD_ID_HERE)
	me = guild.me
	await me.edit(nick="$0")
	await ctx.send("Live Updating Price Starting For XRP")
	called_once_everybit.start("XRP")


@xbot.command(name='sclp', help='stop the clp command')
async def updatingpricestopper(ctx):
	me = ctx.guild.me
	#me = guild.me
	called_once_everybit.cancel()
	print("(XRPHolder) Crypto Live Updating Stopped")
	await ctx.send("Live Price Updating Stopped.")
	#await bot.user.edit(username="BJsCryptoBroker") //Username changing command (Can only be ran once every 2 hours)
	await me.edit(nick="XRPHolder")
	await xbot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="XRP Charts Rise"))
	print("(XRPHolder) Status Set Back")

@xbot.event
async def on_raw_reaction_add(payload):
    if payload.guild_id is None:
        return  # Reaction is on a private message
    guild = xbot.get_guild(payload.guild_id)
    role = discord.utils.get(guild.roles, name="REQUIRED_ROLE_NAME_HERE")
    member = payload.member
    if int(payload.channel_id) == CHANNEL_ID_HERE:
        await member.add_roles(role, reason="User Verfied")
        print ('(RoleManager) Gave role to ' + member.name)


xbot.run(TOKEN)



