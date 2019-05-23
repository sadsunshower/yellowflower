# Code by Nicc
# YellowFlower

# Module: bot
# Main bot module

import asyncio

import discord
import discord.ext.commands

import modules.boredom as boredom
import modules.cats as cats
import modules.handbook as handbook
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

	cats.load_subscriptions(yellow)
	asyncio.create_task(cats.cat_loop(yellow))


# Called when the bot joins a guild
@yellow.event
async def on_guild_join(guild):
	if not yellow.server_settings[str(guild.id)]:
		yellow.server_settings[str(guild.id)] = {}

	await helper.fixed_default_channel(yellow, guild).send('Hi everyone!', embed=helper.embed_happy)


# Called when a member joins a guild the bot is in
@yellow.event
async def on_member_join(member):
	await helper.fixed_default_channel(yellow, member.guild).send('Welcome <@' + str(member.id) + '>!', embed=helper.embed_happy)


# Called when a memeber leaves a guild the bot is in
@yellow.event
async def on_member_remove(member):
	await helper.fixed_default_channel(yellow, member.guild).send(member.name + ' left.', embed=helper.embed_upset)


# Called when the bot recieves a message
@yellow.event
async def on_message(message):
	if re.search(r'(^|\s)i\'?m bored($|\s)', message.content, re.IGNORECASE):
		await message.channel.send(boredom.entertainment())

	await yellow.process_commands(message)


# Keeps track of all current handbook search results messages
handbook_search_results = []


# Called when a reaction is added to a message
@yellow.event
async def on_reaction_add(reaction, user):
	if str(reaction.emoji) != '\U0001f448' and str(reaction.emoji) != '\U0001f449':
		return
	for hsr in handbook_search_results:
		if hsr['message'].id == reaction.message.id and hsr['author'].id == user.id:
			print('bot: DEBUG: paging results')
			start = hsr['current-pos']
			if start > 0 and str(reaction.emoji) == '\U0001f448':
				hsr['current-pos'] -= 15
				start = hsr['current-pos']
			if start + 15 < len(hsr['results']) and str(reaction.emoji) == '\U0001f449':
				hsr['current-pos'] += 15
				start = hsr['current-pos']
			await hsr['message'].edit(content='Searched the handbook for \'' + hsr['search'] + '\':\n```\n' + '\n'.join(hsr['results'][start:start+15]) + '\n```\n Displaying results ' + str(start) + '-' + str(start+15) + ' / ' + str(len(hsr['results'])))
			await reaction.remove(user)


# Handbook command, prints handbook details of a course
@yellow.command(name='handbook', help='Search for information on the UNSW handbook')
async def yhandbook(ctx, *args):
	print('bot: DEBUG: user ' + helper.fixed_username(ctx.message.author.name) + ' ran command handbook')
	
	if not args or len(args) == 0:
		await ctx.channel.send('Please provide a course code')
		return
	
	found = False

	if len(args) == 1:
		query = args[0]

		result = await handbook.handle_query(query)
		if result is not None:
			found = True
			await ctx.channel.send('Handbook entry for **' + query.upper() + '**', embed=discord.Embed(title=result['title'], description=result['description'], url=result['link'], color=helper.embed_colour).add_field(name='Offering Terms', value=result['offerings']).add_field(name='Enrolment Conditions', value=result['conditions']))
			
	if not found:
		# handbook search - eternally under construction
		search = ' '.join(args)

		results = await handbook.handbook_search(search)
		if len(results) < 15:
			await ctx.channel.send('Searched the handbook for \'' + search + '\':\n```\n' + '\n'.join(results) + '\n```')
		else:
			msg = await ctx.channel.send('Searched the handbook for \'' + search + '\':\n```\n' + '\n'.join(results[0:15]) + '\n```\n Displaying results 0-15 / ' + str(len(results)))
			handbook_search_results.append({
				'message' : msg,
				'author' : ctx.message.author,
				'results' : results,
				'search' : search,
				'current-pos' : 0
			})
			await msg.add_reaction('\U0001f448')
			await msg.add_reaction('\U0001f449')


# Cat, subscribes / unsubscribes a user from the daily cat images
@yellow.command(name='cat', help='Subscribe / unsubscribe from daily cat images')
async def cat(ctx):
	print('bot: DEBUG: user ' + helper.fixed_username(ctx.message.author.name) + ' ran command cat')

	if cats.subscribe_unsubscribe(ctx.message.author):
		await ctx.channel.send('<@' + str(ctx.message.author.id) + '> subscribed to daily cat images')
	else:
		await ctx.channel.send('<@' + str(ctx.message.author.id) + '> unsubscribed from daily cat images')


# Sleep - admin command, puts the bot to sleep
# Restricted to (ch)admins
@yellow.command(name='sleep', help='Chadmins only')
async def ysleep(ctx):
	print('bot: DEBUG: user ' + helper.fixed_username(ctx.message.author.name) + ' ran command sleep')

	if ctx.message.author.id in yellow.bot_settings['chadmins']:
		await ctx.channel.send('Good night!')
		os._exit(0)
	else:
		print('bot: DEBUG: chadmins = ' + str(yellow.bot_settings['chadmins']))
		await ctx.channel.send('You must be a chadmin to use that command!')


# Forcecat - admin command, forces a cat image to be fetched and sent to *all* recipients of the daily cat images
# Restricted to (ch)admins
@yellow.command(name='forcecat', help='Chadmins only')
async def forcecat(ctx):
	print('bot: DEBUG: user ' + helper.fixed_username(ctx.message.author.name) + ' ran command forcecat')

	if ctx.message.author.id in yellow.bot_settings['chadmins']:
		await cats.push_cat(yellow)
	else:
		print('bot: DEBUG: chadmins = ' + str(yellow.bot_settings['chadmins']))
		await ctx.channel.send('You must be a chadmin to use that command!')


yellow.server_settings = settings.load_server_settings()
yellow.bot_settings = settings.load_bot_settings()

yellow.run(yellow.bot_settings['discord_token'])
