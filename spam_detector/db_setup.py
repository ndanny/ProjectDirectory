# Run this script to setup a SQLite database with the
# sms, detection and date tables and insert sample data
# into them.

import sqlite3

# Create a connection and a cursor to traverse over our database records
conn = sqlite3.connect('database/spam.sqlite')
curs = conn.cursor()

# Create table spam_db
curs.execute('''CREATE TABLE spam_db
                (sms text, detection integer, date text)''')

# Insert sample values into table
spam = 'Cash in your bonus offer today to receive a FREE pair of skis and a one day pass to Six Flags. Visit www.scam.com.'
ham = 'With atomic and meteoric regards, my volcanic impulse trembles every time I greet a person with a magnitude of character and charm like you.'

curs.execute('''INSERT INTO spam_db
                (sms, detection, date) VALUES
                (?, ?, DATETIME('now'))''', (spam, 1))
curs.execute('''INSERT INTO spam_db
                (sms, detection, date) VALUES
                (?, ?, DATETIME('now'))''', (ham, 0))

# Verify results in the database
curs.execute('''SELECT * FROM spam_db''')
results = curs.fetchall()
print(results)

# Commit and close connection
conn.commit()
conn.close()