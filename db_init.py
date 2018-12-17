"""
This module initializes the database and its tables.
"""

import sqlite3

def create_connection(db_file):
	"""
    Create a database connection to the SQLite database specified by the db_file
	db_file (database file): The database file containing User information

	return: Connection cursor or None
	"""
	try:
		conn = sqlite3.connect(db_file, check_same_thread=False)
		return conn
	except Error as e:
		print(e)

	return None

def initialize(db_file):
	"""
	Initialize the database with the users table.
	db_file (database file): The database file containing User information
	"""
	# Establish the connection
	conn = create_connection("server/users.db")

	# Create the users table
	# Fields: name, email, password
	conn.execute("CREATE TABLE users (email TEXT PRIMARY KEY, name TEXT, password TEXT)")

if __name__ == "__main__":
    initialize("users.db")
