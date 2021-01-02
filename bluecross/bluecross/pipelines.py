import sqlite3
from sqlite3 import Error

class BluecrossPipeline(object):
    def __init__(self):
        self.create_connection()
        #self.create_tables()

    def create_connection(self):
        try:
           self.cxn = sqlite3.connect('rehoming.db')
           self.csr = self.cxn.cursor()
        except Error as e:
            print(e)

    def create_tables(self):
        self.csr.execute("""DROP TABLE IF EXISTS pets""")
        self.csr.execute("""create table pets(
                 petId text,
                 species text,
                 petType text,
                 sex text,
                 age text,
                 centre text,
                 info text,
                 description text,
                 height text,
                 PRIMARY KEY (petId),
                 FOREIGN KEY (centre) REFERENCES centres(centre)
                 )""")

        # primary key is ROWID
        self.csr.execute("""DROP TABLE IF EXISTS adoptions""")
        self.csr.execute("""create table adoptions(                          
                         petId text,
                         reserved bool,
                         dateScraped date,
                         FOREIGN KEY (petId) REFERENCES pets(petId)
                         )""")

        self.csr.execute("""DROP TABLE IF EXISTS centres""")
        self.csr.execute("""create table centres(
                                 centre text,
                                 PRIMARY KEY (centre)
                                 )""")

    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_db(self, item):
        self.csr.execute("""INSERT OR IGNORE INTO pets VALUES (?,?,?,?,?,?,?,?,?)""", (
            item['petId'],
            item['species'],
            item['petType'],
            item['sex'],
            item['age'],
            item['centre'],
            item['info'],
            item['description'],
            item['height']
        ))

        self.csr.execute("""INSERT INTO adoptions VALUES (?,?,?)""", (
            item['petId'],
            item['reserved'],
            item['dateScraped']
        ))

        self.csr.execute("""INSERT OR IGNORE INTO centres VALUES (?)""", (
            item['centre'],
        ))

        self.cxn.commit()
