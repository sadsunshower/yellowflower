# Code by Nicc
# YellowFlower

# Module: helper
# Contains useful global helper functions and objects

import discord

embed_colour = 16777013

embed_happy = discord.Embed(colour=embed_colour).set_image(url = 'https://imgur.com/FfMi4Px.png')
embed_angry = discord.Embed(colour=embed_colour).set_image(url = 'https://imgur.com/cZJYHf1.png')
embed_upset = discord.Embed(colour=embed_colour).set_image(url = 'https://imgur.com/ZrB2i7k.png')


# A fixed method of finding the 'default' text channel in a guild
# Thanks Concord
def fixed_default_channel(yellow, guild):
	channel_id = None
	if yellow.server_settings[str(guild.id)]['active_channel']:
		channel_id = yellow.server_settings[str(guild.id)]['active_channel']

	my_member = None
	for member in guild.members:
		if member.id == yellow.user.id:
			my_member = member

	channel = None
	if channel_id:
		for text_channel in guild.channels:
			if text_channel.id == channel_id:
				channel = text_channel
				break 
	else:
		for text_channel in guild.channels:
			if text_channel.type == discord.ChannelType.text and member.permissions_in(text_channel).send_messages:
				channel = text_channel
				break

	print('helper: DEBUG: default channel for "' + str(guild.name) + '" is "' + str(channel.name) + '"')

	return channel


# Prints a username even if there are non-ascii characters in it
def fixed_username(username):
	return username.encode('ascii', 'ignore').decode('utf-8', 'ignore')


# Only useful once - leaves any servers where there's no server settings entry
# Basically, leave any old servers
async def cleanup(yellow):
	for guild in yellow.guilds:
		if str(guild.id) not in yellow.server_settings:
			print('helper: leaving ' + str(guild.id) + '(' + str(guild.name) + ')')
			await guild.leave()