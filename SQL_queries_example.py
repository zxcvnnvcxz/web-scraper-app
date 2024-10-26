import sqlite3

# Establish a connection and a cursor
connection = sqlite3.connect("./files/data.db")
cursor = connection.cursor()

# Query all data based on a condition
cursor.execute("SELECT * FROM events WHERE date='2088.10.15'")
rows = cursor.fetchall()
print(rows)

# Query certain columns
cursor.execute("SELECT band, date FROM events WHERE date='2088.10.15'")
rows = cursor.fetchall()
print(rows)

# Insert new rows
new_rows = [('Chicken', 'Chicken City', '2088.10.17'), ('Hens', 'Hen City', '2088.10.17')]
cursor.executemany("INSERT INTO events VALUES(?,?,?)", new_rows)
connection.commit()

# Query all data
cursor.execute("SELECT * FROM events")
rows = cursor.fetchall()
print(rows)