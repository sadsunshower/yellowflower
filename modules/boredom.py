# Code by Nicc
# YellowFlower

# Module: boredom
# Provides light entertainment

import os, random, subprocess

# Gets the output of forture, occasionally piping through cowsay
def entertainment():
	f = open('fortune.txt', 'w')

	if random.randint(0, 100) == 0:
		p = subprocess.Popen(['fortune', '-a'], stdout=subprocess.PIPE)
		subprocess.call(['cowsay', '-f', 'bud-frogs'], stdout=f, stdin=p.stdout)
	else:
		subprocess.call(['fortune', '-a'], stdout=f)

	f.close()
	
	f = open('fortune.txt', 'r')
	txt = f.read()
	os.remove('fortune.txt')

	return '```\n' + txt + '\n```'
