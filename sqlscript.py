import sqlite3
conn = sqlite3.connect('catalog.db')

c = conn.cursor()

insert = [
        'insert into categories values (1, "Soccer")',
        'insert into categories values (2, "Basketball")',
        'insert into categories values (3, "Baseball")',
        'insert into categories values (4, "Frisbee")',
        'insert into categories values (5, "Snowboarding")',
        'insert into categories values (6, "Rock Climbing")',
        'insert into categories values (7, "Foosball")',
        'insert into categories values (8, "Skating")',
        'insert into categories values (9, "Hockey")'
        ]

for row in insert:
    c.execute(row)

insert = [
    'insert into items values (1, "Stick", \
            "This game come under hockey", 9)',
    'insert into items values (2, "Goggles", \
            "This game come under hockey", 5)',
    'insert into items values (3, "Snowboard", \
            "This game come under hockey", 5)',
    'insert into items values (4, "Two shinguards", \
            "This game come under hockey", 1)',
    'insert into items values (5, "Shinguards", \
            "This game come under hockey", 1)',
    'insert into items values (6, "Frisbee", \
            "This game come under hockey", 4)',
    'insert into items values (7, "Bat", \
            "This game come under hockey", 3)',
    'insert into items values (8, "Jersey", \
            "This game come under hockey", 1)',
    'insert into items values (9, "Soccer Cleats", \
            "This game come under hockey", 1)',
    'insert into items values (10, "Cricket", \
            "This game come under hockey", 2)'
    ]

for row in insert:
    c.execute(row)

conn.commit()
conn.close()
