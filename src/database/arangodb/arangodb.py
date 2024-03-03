from arango import ArangoClient


class ArangoDB:
    def __init__(self,host:str,username:str,password:str,dbname:str):
        self.client = None
        self.host = host
        self.username = username
        self.password = password
        self.dbname = dbname
    
    @classmethod
    def connect(self)-> ArangoClient:
        if not self.client:
            self.client = ArangoClient(hosts=self.host)
            self.createDbIfNotExist(dbname=self.dbname)
        return self.client
    
    def createDbIfNotExist(self,dbname:str):
        sys_db = self.useDb(dbname='_system', username=self.username, password=self.password)
        if not sys_db.has_database(dbname):
            sys_db.create_database(dbname)
        self.client.db(dbname=dbname)

    def useDb(self,dbname:str):
        return self.client.db(dbname, username=self.username, password=self.password)

arango =  ArangoDB(
    host="http://127.0.0.1:8529",
    username="root",
    password="root",
    dbname="somedb"
)

db = ArangoDB.connect()
