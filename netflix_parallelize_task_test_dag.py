from airflow.sdk import dag, task
import datetime
import time
import random

from trending_on_netflix.netflix_page import NetflixPage
from trending_on_netflix.database.mongodb_client import MongoDBClient
from trending_on_netflix.config import mongo_db_credentials, countries

@dag(
    schedule = None,
    start_date = datetime.datetime.now(),
    catchup = False,
    tags = ["batch-insert", "parallel", "celery"],
)
def netflix_parallelize_task_test_dag():

    @task
    def get_batched_countries():
        countries_to_search = ['Global']+list(countries.keys())
        return [countries_to_search[i:i+15] for i in range(0,len(countries_to_search),15)]
    
    @task
    def fetch_netflix_page(countries:list[str]):
        print(countries,flush=True)
        
        dict_list = []
        for country in countries:
            ntfx_obj = NetflixPage(geography=country)
            dict_list.append(ntfx_obj.get_dict_obj())

        mongo_client = MongoDBClient(
            username = mongo_db_credentials['username'],
            password = mongo_db_credentials['password'],
            ip_add = mongo_db_credentials['ip'],
            port = mongo_db_credentials['port']
            )
        ids = mongo_client.insert('Trending_On_Netflix','Weekly',dict_list)
        print(ids,flush = True)
        # return ntfx_obj.get_dict_obj()
    
    # @task
    # def insert_docs_into_db(ntfx_obj_docs:list[dict]):
    #     mongo_client = MongoDBClient(
    #         username = mongo_db_credentials['username'],
    #         password = mongo_db_credentials['password'],
    #         ip_add = mongo_db_credentials['ip'],
    #         port = mongo_db_credentials['port']
    #         )
    #     print("mongo client created",flush=True)
    #     ids = mongo_client.insert('Trending_On_Netflix','Weekly', ntfx_obj_docs)
        
    #     print(ids,flush = True)

    countries_to_search = get_batched_countries()
    fetch_netflix_page.expand(countries=countries_to_search)
    # insert_docs_into_db(top10_lists)

netflix_parallelize_task_test_dag()