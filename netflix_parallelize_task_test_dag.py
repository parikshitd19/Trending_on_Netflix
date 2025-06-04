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
    '''
    This is a DAG which showcases parallelization of tasks using celery
    '''
    @task
    def get_batched_countries():
        '''
        Divide the Regions into batches of 15
        '''
        countries_to_search = ['Global']+list(countries.keys())
        return [countries_to_search[i:i+15] for i in range(0,len(countries_to_search),15)]
    
    @task
    def fetch_netflix_page(countries:list[str]):
        print(countries,flush=True)

        #Generate the top 10 list for the countries provided
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
        #Insert all the lists in bulk
        ids = mongo_client.insert('Trending_On_Netflix','Weekly',dict_list)
        print(ids,flush = True)

    countries_to_search = get_batched_countries()
    fetch_netflix_page.expand(countries=countries_to_search)

netflix_parallelize_task_test_dag()