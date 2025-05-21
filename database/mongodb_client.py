from .database_client_interface import DatabaseClientInterface
import pymongo
from pymongo.errors import ConnectionFailure


class MongoDBClient(DatabaseClientInterface):
    """
    A MongoDB client to mange the connection & operations to the database
    """
    def __init__(self, ip_add = "localhost", port = "27017", username = "", password = "", url=None):
        
        self.ip_add = ip_add
        self.port = port
        self.username = username
        self.password = password
        self.url = None
        
        if url != None and len(url)>0:
            self.url = url
        else:
            self.url = self.__construct_url()
        
        self.__check_connection_valid()
        

    def __construct_url(self):
        """
        Create the connection url string
        """
        return f"mongodb://{self.username}:{self.password}@{self.ip_add}:{self.port}/"
    
    def __check_connection_valid(self):
        """
        Check if the connection url is valid
        """
        client = pymongo.MongoClient(self.url)
        try:
            # The ping command is cheap and does not require auth.
            client.admin.command('ping')
        except ConnectionFailure:
            print("Server not available")
    
    def __check_if_database_exists(self,database_name):
        """
        Check if a database exists
        """
        mongo_client = pymongo.MongoClient(self.url)
        database_exists = database_name in mongo_client.list_database_names()
        mongo_client.close()
        
        return database_exists
    
    def __check_if_collection_exists(self,database_name,collection_name):
        """
        Check if a collection exists in the specified database
        """
        mongo_client = pymongo.MongoClient(self.url)
        
        if self.__check_if_database_exists(database_name):
            database = mongo_client[database_name]
            coll_exists = collection_name in database.list_collection_names()
            mongo_client.close()
            
            return coll_exists
        
        mongo_client.close()
        
        return False
    
    def insert(self,database_name,collection_name,docs):
        """
        Insert documents in the database
        """
        if self.__check_if_collection_exists(database_name,collection_name):
            mongo_client = pymongo.MongoClient(self.url)
            if type(docs) is not list:
                docs = [docs]
            inserted_id_list = mongo_client[database_name][collection_name].insert_many(docs)
            mongo_client.close()
            return inserted_id_list.inserted_ids
        else:
            raise Exception("Invalid Database or Collection")
    
        
    
    