#!/usr/bin/env python
#
# Started from http://docs.python.org/2/library/sqlite3.html
#
import sqlite3

print "sqlite version {0}".format(sqlite3.sqlite_version)

conn = sqlite3.connect('pyexplore.db')

c = conn.cursor()

# Create table
c.execute('DROP TABLE IF EXISTS purchase')
c.execute('CREATE TABLE purchase (purchasenum integer PRIMARY KEY AUTOINCREMENT, date text, product text, qty integer, extprice real)')

# Insert a row of data
c.execute("INSERT INTO purchase (date, product, qty, extprice) VALUES ('2013-03-17','sunblock',1,6.99)")

# Save (commit) the changes
conn.commit()

# Read one 
t = ('sunblock',)
c.execute('SELECT * FROM purchase WHERE product = ?', t)

print "fetchone returns..."
print c.fetchone()

# Larger example that inserts many records at a time
purchases = [('2013-03-17', 'sunglasses', 1, 45.00),
             ('2013-03-15', 'beach hat', 1, 20.00),
             ('2013-04-06', 'flip flops', 2, 13.00),
            ]
c.executemany('INSERT INTO purchase (date, product, qty, extprice) VALUES (?, ?, ?, ?)', purchases)

print "rows from execute..."
for row in c.execute('SELECT * FROM purchase ORDER BY purchasenum'):
    print row

print "aggregation result..."
for row in c.execute('SELECT date, SUM(extprice) FROM purchase GROUP BY date'):
    print row

print 'aggregation cursor...'
cur = c.execute('SELECT date, COUNT(*) FROM purchase GROUP BY date')
headings = ''
for col in cur.description:
    headings += '{0:20s}'.format(col[0])
print headings
for row in cur:
    rowvalues = ''
    for col in row:
        rowvalues += '{0:20s}'.format(str(col))
    print rowvalues

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()
