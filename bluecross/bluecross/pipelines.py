import pyodbc
import os 

class BluecrossPipeline(object):
    def __init__(self):
        self.create_connection()
        self.create_tables()

    def create_connection(self):
        server = os.environ.get('SQLSERVER')
        database = os.environ.get('SQLDB')
        username = os.environ.get('SQLUSR')
        password = os.environ.get('SQLPSWRD')
        driver = os.environ.get('SQLDRIVER')
        self.cxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
        self.csr = self.cxn.cursor()

    def create_tables(self):
        self.csr.execute("""DROP TABLE IF EXISTS centres""")
        self.csr.execute("""CREATE TABLE centres(
                                 centre nvarchar(450) NOT NULL,
                                 CONSTRAINT pk_centres_centre PRIMARY KEY CLUSTERED (centre) WITH (IGNORE_DUP_KEY = ON)
                                 )""")

        self.csr.execute("""DROP TABLE IF EXISTS pets""")
        self.csr.execute("""CREATE TABLE pets(
                 petId nvarchar(450) NOT NULL,
                 species nvarchar(450) NOT NULL,
                 petType nvarchar(800) NULL,
                 sex nvarchar(450) NOT NULL,
                 age nvarchar(450) NULL,
                 centre nvarchar(450) NOT NULL,
                 info nvarchar(450) NULL,
                 description text NULL,
                 height nvarchar(450) NULL,
                 CONSTRAINT pk_pets_petId PRIMARY KEY CLUSTERED (petId) WITH (IGNORE_DUP_KEY = ON),
                 CONSTRAINT fk_pets_centre FOREIGN KEY (centre) 
                    REFERENCES centres (centre) 
                 )""")

        # primary key is ROWID
        self.csr.execute("""DROP TABLE IF EXISTS adoptions""")
        self.csr.execute("""CREATE TABLE adoptions(                          
                         petId nvarchar(450) NOT NULL,
                         reserved int NOT NULL,
                         dateScraped date NOT NULL,
                         CONSTRAINT fk_adoptions_petId FOREIGN KEY (petId) 
                            REFERENCES pets (petId)
                         )""")


    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_db(self, item):
        self.csr.execute("""INSERT INTO centres VALUES (?)""", (
            item['centre'],
        ))

        self.csr.execute("""INSERT INTO pets VALUES (?,?,?,?,?,?,?,?,?)""", (
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

        self.cxn.commit()
