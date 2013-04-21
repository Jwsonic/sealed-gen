import webapp2
from google.appengine.ext import db
from collections import namedtuple
import csv
import random
import logging

#Formating strings is so much easier than dealing with xml parsing...
card_str = '<card number="{0}" price="0" name="{1}"/>'
deck_file_str = """<?xml version="1.0" encoding="UTF-8"?>
	<cockatrice_deck version="1">
	<deckname></deckname>
	<comments></comments>
	<zone name="main"></zone>
	<zone name="side">{0}</zone>
	</cockatrice_deck>"""

rtr_guilds = ('Azorius', 'Rakdos', 'Selesnya', 'Izzet', 'Golgari')
gtc_guilds = ('Simic', 'Gruul', 'Boros', 'Orzhov', 'Dimir')

colors = {'Azorius':set('UW'), 'Rakdos':set('RB'), 'Selesnya':set('GW'), 'Izzet':set('UR'), 'Golgari':set('GB'), 'Simic':set('UG'), 'Gruul':set('GR'), 'Boros':set('RW'), 'Orzhov':set('BW'), 'Dimir':set('UB')}

#A named tuple for cards to keep things a bit more readable
Card = namedtuple('Card', ['name', 'rarity', 'guild'])

#Load up the sets into lists
with open('rtr-parsed.txt') as f:
	rtr_cards = [Card(name=row[0], rarity=row[1], guild=row[2]) for row in csv.reader(f, delimiter='~')]

with open('gtc-parsed.txt') as f:
	gtc_cards = [Card(name=row[0], rarity=row[1], guild=row[2]) for row in csv.reader(f, delimiter='~')]

with open('dgm-parsed.txt') as f:
	dgm_cards = [Card(name=row[0], rarity=row[1], guild=row[2]) for row in csv.reader(f, delimiter='~')]

#The prerelease promos and their guilds ARE NO LONGER NEEDED
#promos = {'Boros':'Foundry Champion', 'Dimir':'Consuming Aberration', 'Gruul':'Rubblehulk', 'Orzhov':'Treasury Thrull', 'Simic':'Fathom Mage', 'None':None}

def generate_pack(mythics, rares, uncommons, commons, basic_lands=None):

	"""Generate a pack of cards with the distribution as shown by: http://en.wikipedia.org/wiki/Booster_pack. Does not follow print runs."""

	pack = set()

	#A quick lambda to help use find a valid random index
	index = lambda l: random.randrange(0, len(l))

	logging.info('Rares')

	if random.randint(0, 7) is 0: #We've got a 1 in 8 shot our rare is a mythic
		pack.add(mythics[index(mythics)])
	else: #Otherwise it's just a rare :(
		pack.add(rares[index(rares)])
	
	logging.info('uncommons')
	
	while len(pack) < 4: #Add uncommons until we have 4 cards. 1 rare, 3 uncommons. The set will take care of duplicates.
		pack.add(uncommons[index(uncommons)])
	
	logging.info('lands')
	
	if basic_lands: #Add a basic land if there are any
		pack.add(basic_lands[index(basic_lands)])
	
	logging.info('commons {0}'.format(len(commons)))
	
	while len(pack) < 15: #Fill out the pack with commons
		pack.add(commons[index(commons)])

	return pack

def r(cards, rarity):
	"""Returns all the cards in the list that have the given rarity. We do this a lot so it got tossed into a function"""
	return [card.name for card in cards if card.rarity == rarity]

def gen_pack_generator(card_pool):
	"""Yo dawg, returns a function that can be called to generate a pack of the given card_pool"""

	mythics=r(card_pool, 'Mythic Rare')
	rares=r(card_pool, 'Rare')
	uncommons=r(card_pool, 'Uncommon')
	commons=r(card_pool, 'Common')
	basic_lands=r(card_pool, 'Basic Land')

	return lambda: generate_pack(mythics, rares, uncommons, commons, basic_lands)

def gen_guild_pack(guild):
	"""Returns a special guild pack generator"""

	cards = rtr_cards if guild in rtr_guilds else gtc_cards

	return gen_pack_generator([card for card in cards if card.guild.find(guild) > -1])

class MainPage(webapp2.RequestHandler):
	def get(self):
		self.response.write("""
		<!DOCTYPE html>
		<html>
		<body>

		Choose a guild:
		<form action="/" method="post">
		<select name="guild">
		<option value="Simic">Simic</option>
		<option value="Boros">Boros</option>
		<option value="Dimir">Dimir</option>
		<option value="Gruul">Gruul</option>
		<option value="Orzhov">Orzhov</option>
		<option value="Rakdos">Rakdos</option>
		<option value="Selesnya">Selesnya</option>
		<option value="Izzet">Izzet</option>
		<option value="Golgari">Golgari</option>
		<option value="Azorius">Azorius</option>
		</select>
		<br/>
		<input type="submit" value="Build Pool">
		</form>

		</body>
		</html>
		""")

	def post(self):
		guild = self.request.get('guild')

		pool = {}

		logging.info('Generating guild pack')
		#Generate the guild pack
		pack_maker = gen_guild_pack(guild)
		for card in pack_maker():
			if card in pool:
				pool[card] += 1
			else:
				pool[card] = 1

		logging.info('Generating secret guild pack')

		others = gtc_guilds if guild in rtr_guilds else rtr_guilds

		secret_guild = random.choice(others)

		#Grab random guilds from the other set until we have one that shares a color
		while len(colors[guild].intersection(colors[secret_guild])) != 1:
			secret_guild = random.choice(others)

		#Generate the secret guild pack
		pack_maker = gen_guild_pack(secret_guild)
		for card in pack_maker():
			if card in pool:
				pool[card] += 1
			else:
				pool[card] = 1

		logging.info('Generating normal packs')
		#Generate normal packs
	
		pack_maker = gen_pack_generator(dgm_cards)

		for i in range(4):
			for card in pack_maker():
				if card in pool:
					pool[card] += 1
				else:
					pool[card] = 1

		logging.info('Writing response')
		self.response.headers['Content-Type'] = 'text'
		self.response.headers['Content-Disposition'] = 'attachment; filename={0}-{1}_pool.cod'.format(guild, secret_guild)
		self.response.write(deck_file_str.format('\n'.join([card_str.format(number, name) for name, number in pool.items()])))	

app = webapp2.WSGIApplication([('/', MainPage)], debug=True)
