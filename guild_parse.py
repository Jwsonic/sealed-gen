import xml.etree.ElementTree as etree
import sys
import sqlite3

AZORIUS = 'Azorius'
GOLGARI = 'Golgari'
IZZET = 'Izzet'
RAKDOS = 'Rakdos'
SELESNYA = 'Selesnya'

colors = [('UW', AZORIUS), ('GB', GOLGARI), ('UR', IZZET), ('BR', RAKDOS), ('GW', SELESNYA)]
keywords = [('DETAIN', AZORIUS), ('SCAVENGE', GOLGARI), ('OVERLOAD', IZZET), ('UNLEASH', RAKDOS), ('POPULATE', SELESNYA)]

def cost_check(line):
	u = line.upper()

	for c in colors:
		if u.find(c[0][0]) > -1 and u.find(c[0][1]) > -1:
			return c[1]

	return None

def keyword_check(line):
	u = line.upper()

	for keyword in keywords:
		if u.find(keyword[0]) > -1:
			return keyword[1]

	return None

if __name__ == '__main__':
	assert len(sys.argv) > 1, 'You must pass a text file to process'

	with open(sys.argv[1]) as f:
		lines = f.readlines()

		names = [line[6:-1] for line in lines if line.startswith('Name:')]
		rarities = [line[9:-1] for line in lines if line.startswith('Rarity:')]
		
		costs = [cost_check(line) for line in lines if line.startswith('Cost:')]
		keywords = [keyword_check(line) for line in lines if line.startswith('Rules Text:')]

		guilds = [pair[0] or pair[1] or 'None' for pair in zip(costs, keywords)]

		cards = [(names[i], rarities[i], guilds[i]) for i in range(len(names))]

		conn = sqlite3.connect('rtr.sqlite')
		c = conn.cursor()

		c.execute('create table cards (name text, rarity text, guild text)')
		
		for card in cards:
			c.execute('insert into cards values (?, ?, ?)', card)

		conn.commit()
		c.close()
