import sqlite3
from sqlite3 import Error

class BluecrossPipeline(object):
    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        try:
           self.cxn = sqlite3.connect('rehoming.db')
           self.csr = self.cxn.cursor()
        except Error as e:
            print(e)

    def create_table(self):
        self.csr.execute("""DROP TABLE IF EXISTS pet_images""")
        self.csr.execute("""create table pet_images(
                 petType text,
                 reserved text,
                 sex text,
                 age text,
                 location text,
                 info text,
                 refNum text,
                 dateScraped text,
                 description text
                 )""")

    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_db(self, item):
        self.csr.execute("""INSERT INTO pet_images VALUES (?,?,?,?,?,?,?,?,?)""", (
            item['petType'],
            item['reserved'],
            item['sex'],
            item['age'],
            item['location'],
            item['info'],
            item['refNum'],
            item['dateScraped'],
            item['description']
        ))
        self.cxn.commit()
