#General stuff
import discord, logging, json
import asyncio
import os
import traceback, trace
import sysconfig
import typing
import random
import urllib.request, urllib.parse, urllib.error, ssl
import time
import aiohttp
import math
import random
import json
from discord.ext.commands.converter import _get_from_guilds

from discord.guild import Guild

logging.basicConfig(level=logging.WARNING)

from random import seed
from random import randint
from enum import Enum, IntEnum
from discord import Member
from discord.ext.commands import has_permissions, MissingPermissions
from discord.ext import commands
from discord.voice_client import VoiceClient
from discord.utils import get
from discord import Game
from discord.ext.commands import Bot
from async_timeout import timeout
from discord.ext import tasks

logging.basicConfig(level=logging.WARNING)

bot = commands.Bot(command_prefix='.p ')
bot.remove_command('help')
client = discord.Client
author = discord.Member
guild = discord.Guild
message = discord.Message

async def on_ready():
	print(bot.user.name)
	print(bot.user.id)
	print('Is online and running!')
	await bot.change_presence(activity=discord.Game(name="PECK squadron members"))

@bot.event
async def on_message(message):
	await bot.process_commands(message)
	if bot.user.mentioned_in(message) and message.mention_everyone is False:
		await message.channel.send('My prefix is `.p`!')
#Admin stuff
@bot.command(pass_context=True,aliases=['announcement', 'a'])
@commands.has_permissions(administrator=True)
async def Announcement(ctx, *content):
	channel = bot.get_channel(931263111992848395)
	if (ctx.guild.id == 917850361019125820):
		await channel.send(" ".join(content) + "\n-" + ctx.author.mention)

@bot.command(pass_context=True,aliases=['ban'])
@commands.has_permissions(administrator=True)
async def Ban(ctx, member:discord.User=None, reason =None):
	if (member == None or member == ctx.message.author):
		await ctx.channel.send("You cannot ban yourself")
	else:
		await ctx.send(f"`{member}` has been banned!")
		message = f"You have been banned from {ctx.guild.name} for {reason}"
		await member.send(message)
		await ctx.guild.ban(member, reason=reason)

@bot.command(pass_context=True,aliases=["addgroup", "addplatoon", "AddPlatoon"])
@commands.has_permissions(administrator=True)
async def AddGroup(ctx,str1,str2):
	await ctx.send("Creating Group/Platoon role")
	guild = ctx.guild
	await guild.create_role(name=" ".join(str2) +" Member")
	rolename = " ".join(str2)
	await ctx.send(f"Role, called \"{rolename} Member\" has been created")
	categ = await ctx.guild.create_category(str1)
	await guild.create_text_channel('general', category=categ)
	await guild.create_text_channel('roster', category=categ)
	await guild.create_voice_channel('general', category=categ)
	chan1 = discord.utils.get(ctx.guild.channels, name="general", category=categ)
	chan2 = discord.utils.get(ctx.guild.channels, name="roster", category=categ)
	chan3 = discord.utils.get(ctx.guild.voice_channels, name="general", category=categ)
	channel_id1=chan1.id
	channel_id2=chan2.id
	channel_id3=chan3.id
	channelid1=bot.get_channel(channel_id1)
	channelid2=bot.get_channel(channel_id2)
	channelid3=bot.get_channel(channel_id3)
	roles = ctx.guild.roles
	role = get(roles, name=f"{rolename} Member")
	await ctx.send(f"The Group/Platoon, called {str2} has been created")
	await channelid1.set_permissions(ctx.guild.default_role, view_channel=False)
	await channelid1.set_permissions(role, view_channel=True, send_messages=True)
	await channelid2.set_permissions(ctx.guild.default_role, view_channel=False)
	await channelid3.set_permissions(ctx.guild.default_role, view_channel=False)
	await channelid2.set_permissions(role, view_channel=True, send_messages=True)
	await channelid3.set_permissions(role, view_channel=True, connect=True, speak=True)
	await ctx.send("Permissions have been set for the channels")


#Public stuff

@bot.command(pass_context = True , aliases=['h', 'H', 'help'])
async def Help(ctx):	
	embed = discord.Embed(title= 'Command List', description='A bot made by `'+ owner +'` \n Command Prefix .p \n Example: .p help' ,  color=0xeee657)
	embed.add_field(name="[AddPlatoon]", value='Usage: .p AddGroup (Category name) (Role name)')

owner = "Maho_Yoshino#6969"

@bot.command(pass_context=True , aliases=['info', 'I', 'i'])
async def Info(ctx):
	msg = await ctx.send ('Getting information \n This can take a few seconds')
	await asyncio.sleep(random.randrange(1, 5))
	await msg.edit(content=f'-The Ping is `{bot.latency}({round(bot.latency * 1000)}ms)` \n- Made By ' + owner + ', specifically made for the discord server for the -PECK- Order of the Birb squadron')
#error handler and token
class CommandErrorHandler(commands.Cog):
	def _init_(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		if hasattr(ctx.command, 'on_error'):
			return
		ignored = (commands.CommandNotFound, commands.UserInputError)
		error = getattr(error, 'original', error)

		if isinstance(error, commands.DisabledCommand):
			return await ctx.send(f'{ctx.command} has been disabled')

		elif isinstance(error, commands.NoPrivateMessage):
			try:
				return await ctx.author.send(f'{ctx.command} can not be used in Private Messages')

			except:
				pass
		elif isinstance(error, commands.BadArgument):
			if ctx.command.qualified_name == 'tag list':
				return await ctx.send('I could not Find that Member. Please Try again')
				print('>Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
				traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

		@commands.command(name='repeat', aliases=['mimic', 'copy'])
		async def do_repeat(self, ctx, *, inp: str):
			await ctx.send(inp)

		@do_repeat.error
		async def do_repeat_handler(self, ctx, error):
			if isinstance(error, commands.MissingRequiredArgument):
				if error.param.name == 'inp':
					await ctx.send('You forgot to give me Input to Repeat!')

def setup(bot):
	bot.add_cog(CommandErrorHandler(bot))

bot.run('TOKEN HERE')
