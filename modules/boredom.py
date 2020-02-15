# Code by Nicc
# YellowFlower

# Module: boredom
# Provides light entertainment

import random, subprocess

import discord


class Boredom(discord.ext.commands.Cog):
	
	def __init__(self, yellow: discord.ext.commands.Bot):
		self.bot = yellow
	
	@discord.ext.commands.Cog.listener()
	async def on_message(self, message: discord.Message) -> None:
		if not message.content.startswith('im bored'):
			return

		text = ''

		if random.randint(0, 100) == 0:
			p1 = subprocess.Popen(['fortune', '-a'], stdout=subprocess.PIPE)
			p2 = subprocess.call(['cowsay', '-f', 'bud-frogs'], stdout=subprocess.PIPE, stdin=p.stdout)
			text, _ = p2.communicate()
		else:
			p = subprocess.Popen(['fortune', '-a'], stdout=subprocess.PIPE)
			text, _ = p.communicate()
			
		await message.channel.send(f'```\n{text.decode("utf-8", "ignore")}\n```')