
import sys
print("DEBUG sys.path:", sys.path)

import datetime
from airflow.sdk import dag, task
# import sys
# sys.path.append('/opt/airflow/dags/Tending_on_Netflix')
# print("my path", sys.path)
from trending_on_netflix.netflix_page import NetflixPage
from trending_on_netflix.database.mongodb_client import MongoDBClient
from trending_on_netflix.config import mongo_db_credentials

@dag(
    schedule = None,
    start_date = datetime.datetime.now(),
    catchup = False,
    tags = ["example"],
)
def netflix_basic_workflow():
    
    @task(multiple_outputs=True)
    def fetch_netflix_page():
        ntfx_obj = NetflixPage(when = '2025-04-18')
        print(ntfx_obj,flush = True)
        return ntfx_obj.get_dict_obj()
    
    # @task
    # def get_ntfx_obj(ntfx_obj:NetflixPage):
    #     return ntfx_obj.get_dict_obj()
    
    @task
    def insert_doc_into_db(ntfx_obj_doc:dict):
        mongo_client = MongoDBClient(
            username = mongo_db_credentials['username'],
            password = mongo_db_credentials['password'],
            ip_add = mongo_db_credentials['ip'],
            port = mongo_db_credentials['port']
            )
        ids = mongo_client.insert('Trending_On_Netflix','Weekly', ntfx_obj_doc)
        
        print(ids,flush = True)
    
    dict_obj = fetch_netflix_page()
    insert_doc_into_db(dict_obj)

netflix_basic_workflow()
