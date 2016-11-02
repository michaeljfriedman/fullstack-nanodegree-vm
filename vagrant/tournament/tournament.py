#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2 as dbms

# Constants for accessing database
DB_TOURNAMENT 						= "tournament"

TABLE_PLAYERS 						= "players"
COLUMN_PLAYERS_ID 				= "id"
COLUMN_PLAYERS_NAME 			= "name"

TABLE_MATCHES 						= "matches"
COLUMN_MATCHES_ID   			= "id"
COLUMN_MATCHES_WINNER_ID 	= "winner_id"
COLUMN_MATCHES_LOSER_ID 	= "loser_id"

VIEW_PLAYER_WINS					= "player_wins"
VIEW_NUM_MATCHES					= "num_matches"
VIEW_PLAYER_STATS 				= "player_stats"


'''
Connect to the PostgreSQL database. Returns a database connection.
'''
def connect():
	return dbms.connect("dbname=" + DB_TOURNAMENT)


'''
Helper method for deletion. Removes all records from the table passed as
argument.

Args:
	table: name of the table from which records should be removed.
'''
def _deleteFromTable(table):
	db = connect()
	c = db.cursor()
	c.execute("DELETE FROM " + table + ";")
	db.commit()
	db.close()

'''
Remove all the match records from the database.
'''
def deleteMatches():
	_deleteFromTable(TABLE_MATCHES)


'''
Remove all the player records from the database.
'''
def deletePlayers():
	_deleteFromTable(TABLE_PLAYERS)

'''
Returns the number of players currently registered
'''
def countPlayers():
	 db = connect()
	 c = db.cursor()
	 c.execute("SELECT count(*) FROM " + TABLE_PLAYERS + ";")
	 raw_num_players = c.fetchall()
	 return raw_num_players[0][0]

'''
Adds a player to the tournament database.

The database assigns a unique serial id number for the player.  (This
should be handled by your SQL database schema, not in your Python code.)

Args:
	name: the player's full name (need not be unique).
'''
def registerPlayer(name):
	db = connect()
	c = db.cursor()
	c.execute("INSERT INTO " + TABLE_PLAYERS + " (" + COLUMN_PLAYERS_NAME + ") VALUES (%s);", (name,))
	db.commit()
	db.close()

'''
Returns a list of the players and their win records, sorted by wins.

The first entry in the list should be the player in first place, or a player
tied for first place if there is currently a tie.

Returns:
	A list of tuples, each of which contains (id, name, wins, matches):
		id: the player's unique id (assigned by the database)
		name: the player's full name (as registered)
		wins: the number of matches the player has won
		matches: the number of matches the player has played
'''
def playerStandings():
	pass

'''
Records the outcome of a single match between two players.

Args:
	winner:  the id number of the player who won
	loser:  the id number of the player who lost
'''
def reportMatch(winner, loser):
	db = connect()
	c = db.cursor()
	c.execute("INSERT INTO " + TABLE_MATCHES + " (" + COLUMN_MATCHES_WINNER_ID + ", "
		+ COLUMN_MATCHES_LOSER_ID + ") VALUES (%s, %s);", (winner, loser))
	db.commit()
	db.close()
 
'''
Returns a list of pairs of players for the next round of a match.
	
Assuming that there are an even number of players registered, each player
appears exactly once in the pairings.  Each player is paired with another
player with an equal or nearly-equal win record, that is, a player adjacent
to him or her in the standings.

Returns:
	A list of tuples, each of which contains (id1, name1, id2, name2)
		id1: the first player's unique id
		name1: the first player's name
		id2: the second player's unique id
		name2: the second player's name
'''
def swissPairings():
	pass

if __name__ == '__main__':
	pass