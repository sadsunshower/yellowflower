# Code by Nicc
# YellowFlower

# Module: handbook
# Scrapes the UNSW handbook for course information

import discord

import re, typing

from modules.newhandbook.description import fetch_description
from modules.newhandbook.info import HandbookDetails
from modules.newhandbook.utilisation import fetch_utilisation

import modules.helper as helper


def handbook_embed(course_info: HandbookDetails) -> discord.Embed:
	embed = discord.Embed(colour=helper.embed_colour, title=course_info.title, description=course_info.description, url=course_info.url)
	embed.set_footer(text='YellowFlower Handbook Command - Using UNSW 2020 Handbook')
	embed.set_thumbnail(url='https://yt3.ggpht.com/a/AGF-l7_fK0Hy4B4JO8ST-uGqSU69OTLHduk4Kri_fQ=s288-c-k-c0xffffffff-no-rj-mo')

	embed.add_field(name='Offerings', value=course_info.offering, inline=False)
	
	if course_info.conditions is not None:
		embed.add_field(name='Requirements', value=course_info.conditions, inline=False)
	
	if course_info.equivalent is not None:
		embed.add_field(name='Equivalent Courses', value=course_info.equivalent, inline=False)
	
	if course_info.exclusion is not None:
		embed.add_field(name='Exclusion Courses', value=course_info.exclusion, inline=False)
	
	return embed


def utilisation_embed(code: str, term: str, classes: typing.List[typing.Dict[str, str]]) -> discord.Embed:
	embed = discord.Embed(colour=helper.embed_colour, title=f'{code} {term}', description=f'The following classes are available for {code} in {term}')
	embed.set_footer(text='YellowFlower Handbook Command - Using UNSW 2020 Class Utilisation')
	embed.set_thumbnail(url='https://yt3.ggpht.com/a/AGF-l7_fK0Hy4B4JO8ST-uGqSU69OTLHduk4Kri_fQ=s288-c-k-c0xffffffff-no-rj-mo')

	for class_info in classes:
		class_type = {
			'LEC' : 'Lecture',
			'TUT' : 'Tutorial',
			'LAB' : 'Laboratory',
			'TLB' : 'Tutorial / Laboratory',
			'SEM' : 'Seminar',
			'OTH' : 'Other'
		}.get(class_info['type'], 'Unknown')

		class_status = 'Unknown \U0001F62E'

		if class_info['status'] == 'Open':
			enrolled = int(class_info['enrolled'])
			capacity = int(class_info['capacity'])
			full = 100.0 * enrolled / capacity

			class_status = f'Open ({enrolled}/{capacity} - {full:.1f}% full) '

			if full > 95.0 or capacity - enrolled <= 1:
				class_status += '\U0001F631'
			elif full > 75.0 or capacity - enrolled <= 3:
				class_status += '\U0001F623'
			elif full > 50.0:
				class_status += '\U0001F642'
			else:
				class_status += '\U0001F60C'
		elif class_info['status'] == 'Closed':
			class_status = 'Closed \U0001F634'
		elif class_info['status'] == 'Canc':
			class_status = 'Cancelled \U0001F622'
		elif class_info['status'] == 'Tent':
			class_status = 'Tentative \U0001F914'
		elif class_info['status'] == 'Full':
			class_status = 'Full \U0001F624'

		embed.add_field(name=f'{class_type} {class_info["name"]} ({class_info["code"]})', value=class_status, inline=False)
	
	return embed


class Handbook(discord.ext.commands.Cog):

	def __init__(self, yellow: discord.ext.commands.Bot):
		self.bot = yellow
	
	@discord.ext.commands.command(name='handbook', help='Search for information on the UNSW handbook')
	async def handbook(self, ctx: discord.ext.commands.Context, *args):
		if not args or len(args) == 0 or not re.fullmatch(r'[a-zA-Z]{4}[0-9]{4}', args[0]):
			await ctx.channel.send('Please provide a valid course code, e.g. COMP2041')
			return
		
		info = fetch_description(2020, args[0].upper())

		if info is None:
			await ctx.channel.send(f'Could not find any information on \'{args[0].upper()}\'')
		else:
			await ctx.channel.send('', embed=handbook_embed(info))
	
	@discord.ext.commands.command(name='util', help='Search for class utilisation information')
	async def util(self, ctx: discord.ext.commands.Context, *args):
		if not args or len(args) < 2 or not re.fullmatch(r'[a-zA-Z]{4}[0-9]{4}', args[0]) or not re.fullmatch(r'[TU][123]', args[1]):
			await ctx.channel.send('Please provide a valid course code and term')
			return
		
		classes = fetch_utilisation(args[1].upper(), args[0].upper())

		if classes is None:
			await ctx.channel.send(f'Could not find any information on \'{args[0].upper()}\' in {args[1].upper()}')
		else:
			await ctx.channel.send('', embed=utilisation_embed(args[0].upper(), args[1].upper(), classes))