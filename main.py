import webapp2
from google.appengine.ext import db
from collections import namedtuple
import csv
import random
import logging

card_str = '<card number="{0}" price="0" name="{1}"/>'
deck_file_str = """<?xml version="1.0" encoding="UTF-8"?>
	<cockatrice_deck version="1">
	<deckname></deckname>
	<comments></comments>
	<zone name="main"></zone>
	<zone name="side">{0}</zone>
	</cockatrice_deck>"""

promos = {'Azorius':'Archon of the Triumvirate', 'Izzet':'Hypersonic Dragon', 'Rakdos':'Carnival Hellsteed', 'Golgari':'Corpsejack Menace', 'Selesnya':'Grove of the Guardian', 'None':None}

Card = namedtuple('Card', ['name', 'rarity', 'guild'])

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

with open('cards.txt') as f:
	cards = [Card(name=row[0], rarity=row[1], guild=row[2]) for row in csv.reader(f, delimiter='~')]

def r(cards, rarity):
	return [card.name for card in cards if card.rarity == rarity]

def gen_pack(card_pool):
	"""Generate a normal pack of cards for sealed"""
	return generate_pack(mythics=(card_pool, 'Mythic Rare'), rares=r(card_pool, 'Rare'), uncommons=r(card_pool, 'Uncommon'), commons=r(card_pool, 'Common'), basic_lands=r(card_pool, 'Basic Land'))

class MainPage(webapp2.RequestHandler):
	def get(self):
		self.response.write("""
		<!DOCTYPE html>
		<html>
		<body>

		Choose a guild:
		<form action="/" method="post">
		<select name="guild">
		<option value="Azorius">Azorius</option>
		<option value="Golgari">Golgari</option>
		<option value="Izzet">Izzet</option>
		<option value="Selesnya">Selesnya</option>
		<option value="Rakdos">Rakdos</option>
		<option value="None">None</option>
		</select>
		<br/>
		<input type="submit" value="Build Pool">
		</form>

		</body>
		</html>
		""")

	def post(self):
		guild = self.request.get('guild')
		self.response.headers['Content-Type'] = 'text'
		self.response.headers['Content-Disposition'] = 'attachment; filename={0}_pool.cod'.format(guild)
	
		logging.info('Getting guild cards')
		#get the cards for our guilds
		guild_cards = [card for card in cards if card.guild.find(guild) > -1]

		logging.info('Guld len: {0}'.format(len(guild_cards)))

		pool = {}

		logging.info('Adding promo')
		#Add this guild's promo
		pool[promos[guild]] = 1

		logging.info('Generating guild pack')
		#Generate the guild pack
		for card in gen_pack(guild_cards):
			if card in pool:
				pool[card] += 1
			else:
				pool[card] = 1

		logging.info('Generating normal packs')
		#Generate normal packs
		for i in range(5):
			for card in gen_pack(cards):
				if card in pool:
					pool[card] += 1
				else:
					pool[card] = 1

		logging.info('Writing response')
		self.response.write(deck_file_str.format('\n'.join([card_str.format(number, name) for name, number in pool.items()])))	



app = webapp2.WSGIApplication([('/', MainPage)], debug=True)
