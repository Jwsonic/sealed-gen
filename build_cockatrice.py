#!/usr/bin/python3.3
from bs4 import BeautifulSoup
import requests
import argparse

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
			images[link.get('alt')] = link.get('src')

	#Ship it back
	return images

def findcardtype(cardtext):
	"""Takes card text as a string and returns the card type as a string"""

	return ''

def buildcardxml(cardfile, cardimages):
	"""Read in the card info, then stick it into some xml"""

	#Read in all the card data
	with open(cardfile) as f:
		cardtext = f.read()

	for card in cardtext.split('\n\n'):
		pass	


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
