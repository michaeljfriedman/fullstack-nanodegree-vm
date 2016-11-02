#
# Database access functions for the web forum.
# 

import time
import psycopg2 as dbms
import bleach

# Database constants
DB_NAME = "forum"

# 'posts' table constants
TABLE_POSTS = "posts"
COLUMN_CONTENT = "content"
COLUMN_TIME = "time"
COLUMN_ID = "id"

'''
Gets all the posts from the database, sorted with the newest first.

Returns:
A list of dictionaries. This list corresponds to the table, and each
dictionary entry corresponds to a column of that table. Each dictionary has a
'content' key pointing to the post content, and 'time' key pointing to the
time it was posted. The list is sorted by the the 'time' key of each dictionary,
from latest to earliest time.
'''
def GetAllPosts():
	# Query database
	selector = "%s, %s" % (COLUMN_CONTENT, COLUMN_TIME)
	db = dbms.connect("dbname=%s" % (DB_NAME))
	c = db.cursor()
	c.execute("SELECT " + selector + " FROM " + TABLE_POSTS + " ORDER BY " + COLUMN_TIME + " DESC;")
	raw_posts = c.fetchall()
	db.close()

	# Convert from raw data format to list of dictionaries
	idx_content = 0
	idx_time    = 1
	posts = [{ "content": raw_post[idx_content], "time": raw_post[idx_time] } 
							for raw_post in raw_posts]
	return posts

'''
Adds a new post to the database.

Args:
	content: The text content of the new post.

Returns:
	void
'''
def AddPost(content):
	# Clean content of potential spam
	clean_content = str(bleach.clean(content))
	
	# Query database
	db = dbms.connect('dbname=%s' % (DB_NAME))
	c = db.cursor()
	c.execute("INSERT INTO " + TABLE_POSTS + " (" + COLUMN_CONTENT + ") VALUES (%s);", (clean_content,))
	db.commit()
	db.close()