import sqlite3
import sys

AZORIUS = 'Azorius'
GOLGARI = 'Golgari'
IZZET = 'Izzet'
RAKDOS = 'Rakdos'
SELESNYA = 'Selesnya'
SIMIC = 'Simic'
BOROS = 'Boros'
DIMIR = 'Dimir'
GRUUL = 'Gruul'
ORZHOV = 'Orzhov'

#colors = [('UW', AZORIUS), ('GB', GOLGARI), ('UR', IZZET), ('BR', RAKDOS), ('GW', SELESNYA)]
#keywords = [('DETAIN', AZORIUS), ('SCAVENGE', GOLGARI), ('OVERLOAD', IZZET), ('UNLEASH', RAKDOS), ('POPULATE', SELESNYA)]

colors = [('UG', SIMIC), ('UB', DIMIR), ('WR', BOROS), ('GR', GRUUL), ('WB', ORZHOV), ('UW', AZORIUS), ('GB', GOLGARI), ('UR', IZZET), ('BR', RAKDOS), ('GW', SELESNYA)]
keywords = [('EVOLVE', SIMIC), ('CYPHER', DIMIR), ('BATTALION', BOROS), ('BLOODRUSH', GRUUL), ('EXTORT', ORZHOV), ('DETAIN', AZORIUS), ('SCAVENGE', GOLGARI), ('OVERLOAD', IZZET), ('UNLEASH', RAKDOS), ('POPULATE', SELESNYA)]

def cost_check(line):
	"""Check the mana cost for guild affiliation"""
	u = line.upper()

	guilds = set()

	for c in colors:
		if u.find(c[0][0]) > -1 and u.find(c[0][1]) > -1: #solidly in one guild
			return c[1]
		elif u.find(c[0][0]) > -1 or u.find(c[0][1]) > -1: #in two guilds
			guilds.add(c[1])

	if len(guilds) == 0:
		return None

	return '|'.join(guilds)

def keyword_check(line):
	"""Check the text box for guild affiliation"""
	u = line.upper()

	for keyword in keywords:
		if u.find(keyword[0]) > -1:
			return keyword[1]

	return None

if __name__ == '__main__':
	assert len(sys.argv) > 1, 'You must pass a text file to process'

	with open(sys.argv[1], encoding='utf-8') as f:
		lines = f.readlines()

		names = [line[6:-1] for line in lines if line.startswith('Name:')]
		rarities = [line[9:-1] for line in lines if line.startswith('Rarity:')]	
		costs = [cost_check(line) or 'None' for line in lines if line.startswith('Cost:')]

		print('names: {0}, rarity: {1}, cost: {2}'.format(len(names), len(rarities), len(costs)))

		cards = ['{0}~{1}~{2}'.format(names[i], rarities[i], costs[i]) for i in range(len(names))]

		with open(sys.argv[1][:-4] + '-parsed.txt', 'w') as f:
			f.write('\n'.join(cards))
				
