import webapp2
from google.appengine.ext import db

class App(db.Model):
	app_name = db.StringProperty(required=True)
	bucket_name = db.StringProperty(required=True) 

class Image(db.Model):
	name = db.StringProperty(required=True)
	last_shown = db.DateProperty(required=True)

class Card(db.Model):
	name = db.StringProperty(required=True)
	rarity = db.StringProperty(required=True)
	guild = db.StringProperty()
	set = db.StringProperty(required=True)


class UploadCards(webapp2.RequestHandler):
	def post(self): #Handle posts of images
		
		name = self.request.get('name')
		rarity = self.request.get('rarity')
		guild = self.request.get('guild')
		set = self.request.get('set')

		if guild == '': guild = None

		if name != '' and rarity != '' and set != '':
			card = Card(name=name, rartiy=rarity, set=set, guild=guild)

			card.put()
		else:
			self.response.write('Missing parameters!')

	def get(self):
		self.response.write('\n'.join([card.name for card in card.All()]))

class AppCreator(webapp2.RequestHandler):
	def post(self):
		name = self.request.get('APP_NAME')
		bucket = self.request.get('BUCKET')

		if name != '' and bucket != '':
			app = App.all().filter("app_name = ", name).get()

			if app is not None: #The app already exists
				self.response.write('App already exists!')
			else: #We need to make a new app
				app = App(app_name=name, bucket_name=bucket)
				app.put()

				self.response.write('Success!\n')
		else:
			self.response.write('Missing required data!\n')

	def get(self):
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.write('\n'.join(['{0}: {1}'.format(app.app_name, app.bucket_name) for app in App.all()]))

class ImageChooser(webapp2.RequestHandler):
	"""This class chooses a new image for each app"""

	def get(self):
		self.response.headers['Content-Type'] = 'text/plain'

		self.response.write('Today\'s new images:\n')

		for app in App.all(): #We need to get a new image for every app
			today_image = next(Image.all().ancestor(app.key()).order('last_shown').run(limit=1))

			today_image.last_shown = date.today()
			today_image.put()

			#Write out the new image
			self.response.write('{0}: {1}\n'.format(app.app_name, today_image.name))

			conn = S3Connection()
			
			#Update the S3 text file
			k = Key(conn.get_bucket(app.bucket_name))
			k.key = 'today.txt'
			k.set_contents_from_string(today_image.name)
			k.set_acl('public-read')


app = webapp2.WSGIApplication([	('/', MainPage), 
																('/upload', UploadCards),
																('/new', ImageChooser)], debug=True)
