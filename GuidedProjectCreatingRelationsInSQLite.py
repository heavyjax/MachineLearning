import sqlite3

conn = sqlite3.connect('/Users/heavyjax/GoogleDrive/MachineLearning/Dataquest/GuidedProjectPreparingDataForSQLite/data/nominations.db')
#Explore nominations.db
schema = conn.execute('PRAGMA TABLE_INFO(NOMINATIONS)').fetchall()
first_ten = conn.execute('SELECT * FROM NOMINATIONS LIMIT 10').fetchall()

#Create table CEREMONIES and insert values into it
conn.execute('CREATE TABLE CEREMONIES(id integer PRIMARY KEY, Year integer, Host text);')
years_hosts = [
    (2010, "Steve Martin"),
    (2009, "Hugh Jackman"),
    (2008, "Jon Stewart"),
    (2007, "Ellen DeGeneres"),
    (2006, "Jon Stewart"),
    (2005, "Chris Rock"),
    (2004, "Billy Crystal"),
    (2003, "Steve Martin"),
    (2002, "Whoopi Goldberg"),
    (2001, "Steve Martin"),
    (2000, "Billy Crystal"),
]
insert_query = "INSERT INTO CEREMONIES (Year, Host) VALUES (?,?);"
conn.executemany(insert_query, years_hosts)
#conn.execute('drop table ceremonies')

ceremonies = conn.execute('select * from ceremonies').fetchall()
#print(conn.execute('pragma table_info(ceremonies)').fetchall())
#for i in ceremonies:
    #print(i)

#Turn on foreign key constraints. Using to prevent us from inserting rows with nonexisting foreign key values
conn.execute('PRAGMA foreign_keys = ON;')

conn.execute('CREATE TABLE NOMINATIONS_TWO(id integer PRIMARY KEY, category text, nominee text, movie text, character text, won text, ceremony_id integer, foreign key (ceremony_id) references ceremonies (id));')
nominations_two = conn.execute('pragma table_info(nominations_two)').fetchall()
#for i in nominations_two:
    #print(i)
joined_nominations = conn.execute('SELECT nominations.category, nominations.nominee, nominations.movie, nominations.character, nominations.won, ceremonies.id FROM nominations INNER JOIN ceremonies ON nominations.year == ceremonies.year;').fetchall()
#for i in joined_nominations:
    #print(i)
insert_query_two = "INSERT INTO NOMINATIONS_TWO (category, nominee, movie, character, won, ceremony_id) VALUES (?,?,?,?,?,?);"
conn.executemany(insert_query_two, joined_nominations)
#nominations_two = conn.execute('pragma table_info(nominations_two)').fetchall()
#nominations_two = conn.execute('select * from nominations_two').fetchall()
#conn.execute('drop table nominations')
conn.execute('ALTER TABLE NOMINATIONS_TWO RENAME TO NOMINATIONS')
#for i in nominations_two:
    #print(i)

conn.execute('CREATE TABLE MOVIES(id integer PRIMARY KEY, Movie text)')
conn.execute('CREATE TABLE ACTORS(id integer PRIMARY KEY, Actor text)')
conn.execute('CREATE TABLE MOVIES_ACTORS(id integer PRIMARY KEY, Movie_id integer references MOVIES (id), Actor_id integer references ACTORS (id)')
#conn.execute('CREATE TABLE movies_actors (id INTEGER PRIMARY KEY, movie_id INTEGER REFERENCES movies(id), actor_id INTEGER REFERENCES actors(id));')
