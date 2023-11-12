# Import required modules
import csv
import sqlite3
 
# Connecting to the geeks database
connection = sqlite3.connect('database/db.sqlite3')
cursor = connection.cursor()

file = open('Revives_update.csv')
 
contents = csv.reader(file)
 
insert_records = "INSERT INTO kits_revticket (createdAt, updatedAt, modName, userName, steamId, growth, dinoName, ticketLink, revd) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);"
 
cursor.executemany(insert_records, contents)
print(connection.total_changes)

connection.commit()
connection.close()