import sqlite3
conn = sqlite3.connect('catalog.db')

c = conn.cursor()


delete = 'delete from items'
c.execute(delete)
delete = 'delete from categories'
c.execute(delete)


insert = ['insert into user (id, name, email) values (1, "Bharath", "bharath.mylarappa1@gmail.com")']
for row in insert:
    c.execute(row)

insert = [
        'insert into categories values (1, "Soccer", 1)',
        'insert into categories values (2, "Basketball", 1)',
        'insert into categories values (3, "Baseball", 1)',
        'insert into categories values (4, "Frisbee", 1)',
        'insert into categories values (5, "Snowboarding", 1)',
        'insert into categories values (6, "Rock Climbing", 1)',
        'insert into categories values (7, "Foosball", 1)',
        'insert into categories values (8, "Skating", 1)',
        'insert into categories values (9, "Hockey", 1)'
        ]

for row in insert:
    c.execute(row)

insert = [
    'insert into items values (1, "Stick", \
            "This game come under hockey", 9, 1)',
    'insert into items values (2, "Goggles", \
            "This game come under hockey", 5, 1)',
    'insert into items values (3, "Snowboard", \
            "This game come under hockey", 5, 1)',
    'insert into items values (4, "Two shinguards", \
            "This game come under hockey", 1, 1)',
    'insert into items values (5, "Shinguards", \
            "This game come under hockey", 1, 1)',
    'insert into items values (6, "Frisbee", \
            "This game come under hockey", 4, 1)',
    'insert into items values (7, "Bat", \
            "This game come under hockey", 3, 1)',
    'insert into items values (8, "Jersey", \
            "This game come under hockey", 1, 1)',
    'insert into items values (9, "Soccer Cleats", \
            "This game come under hockey", 1, 1)',
    'insert into items values (10, "Cricket", \
            "This game come under hockey", 2, 1)'
    ]

for row in insert:
    c.execute(row)

conn.commit()
conn.close()
