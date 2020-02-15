# Code by Nicc
# YellowFlower

# Module: bot
# Main bot module

import asyncio

import discord

import modules.boredom as boredom
import modules.handbook as handbook

from modules.boredom import Boredom
from modules.handbook import Handbook

import modules.helper as helper
import modules.settings as settings

import os, random, re

yellow = discord.ext.commands.Bot(command_prefix='&')


# Called when the bot is 'ready'
@yellow.event
async def on_ready():
	print('bot: started')
	print('bot: add me with https://discordapp.com/oauth2/authorize?client_id=' + str(yellow.user.id) + '&scope=bot')

	await helper.cleanup(yellow)

	await yellow.change_presence(activity=discord.Game(name='drinking tea'))


# Called when the bot joins a guild
@yellow.event
async def on_guild_join(guild: discord.Guild):
	if not yellow.server_settings[str(guild.id)]:
		yellow.server_settings[str(guild.id)] = {}
		settings.save_server_settings(yellow.server_settings)

	await helper.fixed_default_channel(yellow, guild).send('Hi everyone!', embed=helper.embed_happy)


# Called when a member joins a guild the bot is in
@yellow.event
async def on_member_join(member: discord.Member):
	await helper.fixed_default_channel(yellow, member.guild).send('Welcome <@' + str(member.id) + '>!', embed=helper.embed_happy)


# Called when a memeber leaves a guild the bot is in
@yellow.event
async def on_member_remove(member: discord.Member):
	await helper.fixed_default_channel(yellow, member.guild).send(member.name + ' left.', embed=helper.embed_upset)


# Sleep - admin command, puts the bot to sleep
# Restricted to (ch)admins
@yellow.command(name='sleep', help='Chadmins only')
async def ysleep(ctx: discord.ext.commands.Context):
	print('bot: DEBUG: user ' + helper.fixed_username(ctx.message.author.name) + ' ran command sleep')

	if ctx.message.author.id in yellow.bot_settings['chadmins']:
		await ctx.channel.send('Good night!')
		os._exit(0)
	else:
		print('bot: DEBUG: chadmins = ' + str(yellow.bot_settings['chadmins']))
		await ctx.channel.send('You must be a chadmin to use that command!')


yellow.add_cog(Handbook(yellow))
yellow.add_cog(Boredom(yellow))

yellow.server_settings = settings.load_server_settings()
yellow.bot_settings = settings.load_bot_settings()

yellow.run(yellow.bot_settings['discord_token'])