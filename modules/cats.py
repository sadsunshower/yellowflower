# Code by nicc
# YellowFlower

# Module: cats
# Cats by subscription

import asyncio

import modules.helper as helper

import discord

import datetime, json, requests


subscriptions = {}

sent = []


def get_cat():
	resp = requests.get('https://aws.random.cat/meow')
	return resp.json()['file']


async def cat_loop(yellow):
	while True:
		await check(yellow)
		await asyncio.sleep(30*60)


async def check(yellow):
	if str(datetime.date.today()) in sent:
		print('cats: DEBUG: catcheck bypassed (already sent)')
		return

	current = datetime.datetime.now()
	
	lower = datetime.datetime.now().replace(hour=23, minute=0)

	if lower <= current:
		sent.push(str(datetime.date.today()))
		await push_cat(yellow)
	else:
		print('cats: DEBUG: catcheck at ' + str(current) + ' failed (too early)')


async def push_cat(yellow):
	cat = get_cat()

	print('cats: DEBUG: sending ' + cat + '...')

	for uid in subscriptions:
		print('cats: DEBUG: sending to ' + uid + ' (name ' + subscriptions[uid].name + ')')
		await subscriptions[uid].send('', embed=discord.Embed(colour=helper.embed_colour).set_image(url=cat).set_footer(text='Provided by https://aws.random.cat/meow'))


def subscribe_unsubscribe(user):
	global subscriptions

	if str(user.id) in list(subscriptions):
		del subscriptions[str(user.id)]
	else:
		subscriptions[str(user.id)] = user

	save_subscriptions()
	return str(user.id) in subscriptions


def save_subscriptions():
	subscriptions_copy = {}
	for uid in subscriptions:
		subscriptions_copy[uid] = None

	with open('data/cat_subscriptions.json', 'w') as f:
		f.write(json.dumps(subscriptions_copy))


def load_subscriptions(yellow):
	global subscriptions

	with open('data/cat_subscriptions.json', 'r') as f:
		subscriptions = json.loads(f.read())

	for g in yellow.guilds:
		for m in g.members:
			if str(m.id) in subscriptions:
				subscriptions[str(m.id)] = m

	for uid in list(subscriptions):
		if subscriptions[uid] is None:
			del subscriptions[uid]