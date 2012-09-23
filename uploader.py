import sqlite
import sys

if __name__ == '__main__':
	assert len(sys.argv) > 1, 'You must pass a db parameter!'

	sqlite3.connect(sys.argv[1])
	c = conn.cursor()

	for card in c.execut('select * from cards'):
		#upload stuff here

	c.close()
