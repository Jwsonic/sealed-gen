#!/usr/bin/python3.3
from bs4 import BeautifulSoup
import requests
import argparse
import re

#Different card types
CREATURE_TYPE = 'Creature'
ENCHANTMENT_TYPE = 'Enchantment'
SORCERY_TYPE = 'Sorcery'
INSTANT_TYPE = 'Instant'
PLANESWALKER_TYPE = 'Planeswalker'
LAND_TYPE = 'Land'
ARTIFACT_TYPE = 'Artifact'

def getcardimages(page):
	"""Get all the card images as a dict with name:url as the scheme"""

	#Empty dict to hold the pairings
	images = {}

	#Build up a soup object
	r = requests.get(page)
	soup = BeautifulSoup(r.text)

	#Build out the dictionary
	for link in soup.find_all('img', 'article-image'): 
		if link.get('alt') is not None:
			images[link.get('alt').replace("’", "'").replace("Æ", "AE")] = link.get('src')

	#Ship it back
	return images

def buildcardxml(cardfile, cardimages, setname='GTC'):
	"""Read in the card info, then stick it into some xml"""

	#Read in all the card data
	with open(cardfile) as f:
		cardtext = f.read()

	#Hybrib mana fix
	for pair in [('{ub}', '(U/B)'), ('{wb}', '(W/B)'), ('{gu}', '(G/U)'), ('{rg}', '(R/G)'), ('{rw}', '(R/W)')]:
		cardtext = cardtext.replace(pair[0], pair[1])

	#Card colors
	colors = set('WURBG')
	cards = []

	#Break up text into card groups
	for cardtext in cardtext.split('\n\n'):

		cardtype = re.search(r'Type:\t(.+)\n', cardtext).groups()[0]
		name = re.search(r'Name:\t(.+)\n', cardtext).groups()[0]
		cost = re.search(r'Cost:\t (.+)\n', cardtext)
		text = re.search(r'Rules Text:\t (.+)Flavor', cardtext, re.DOTALL) or re.search(r'Rules Text:\t (.+)Illus.', cardtext, re.DOTALL)

		if text is None:
			text = ''
		else:
			text = text.groups()[0]

		#Handle lands
		if cost is None:
			cost = ''
		else:
			cost = cost.groups()[0].upper()

		#Grab the xml
		xml = '<card><name>{0}</name><set picURL="{1}" picURLHq="" picURLSt="">{2}</set><type>{3}</type><manacost>{4}</manacost><text>{5}</text>'.format(name, cardimages[name], setname, cardtype, cost, text)

		#Find out what colors we are
		cardcolors = colors & set(cost)

		#Add the colors to the xml
		for color in cardcolors:
			xml += '<color>{0}</color>'.format(color)

		if cardtype.find(CREATURE_TYPE) > -1:
			power = re.search(r'Pow/Tgh:\t (.+)\n', cardtext).groups()[0]
			
			#Handle creature specific stuff
			xml += '<tablerow>2</tablerow><pt>{0}</pt>'.format(power)
		elif cardtype.find(PLANESWALKER_TYPE) > -1:
			loyalty = re.search(r'Pow/Tgh:\t (.+)\n', cardtext).groups()[0]

			#Handle planeswalker specific stuff
			xml += '<tablerow>1</tablerow><loyalty>{0}</loyalty>'.format(loyalty)
		elif cardtype.find(ENCHANTMENT_TYPE) > -1 and cardtype.find('Aura') == -1:
			xml += '<tablerow>1</tablerow>'
		elif cardtype.find(SORCERY_TYPE) > -1 or cardtype.find(INSTANT_TYPE) > -1:
			xml += '<tablerow>3</tablerow>'
		else:
			xml += '<tablerow>2</tablerow>'

		#Append the xml to the list
		cards.append(xml + '</card>')	

	return cards

if __name__ == '__main__':
	#Build a parser for the args passed in
	parser = argparse.ArgumentParser()

	#-c CARDFILE -p PAGE -o OUTFILE
	parser.add_argument("-c", "--cardfile", help="Card text file")
	parser.add_argument("-p", "--page", help="Image Spoiler Page")
	parser.add_argument("-o", "--output", help="Output file")

	#Parse the args that were passed to us
	args = parser.parse_args()

	#Make sure we've got some sane input
	cardfile = args.cardfile or 'cards.txt'
	page = args.page or 'http://wizards.com/Magic/TCG/article.aspx?x=mtg/tcg/gatecrash/cig#'
	outfile = args.output or 'cockatrice_patch.xml'

	#Grab the card images
	cardimages = getcardimages(page)

	#Build up some text xml for the out file
	cardxml = buildcardxml(cardfile, cardimages)

	#Write the xml to the out file
	with open(outfile, 'w') as f:
		f.write('\n'.join(cardxml))
