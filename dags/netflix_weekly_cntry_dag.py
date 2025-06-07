from airflow.decorators import dag, task
from airflow.operators.empty import EmptyOperator
# from airflow.utils.trigger_rule import TriggerRule
import datetime

from trending_on_netflix.netflix_page import NetflixPage
from trending_on_netflix.database.mongodb_client import MongoDBClient
from trending_on_netflix.config import mongo_db_credentials, countries, country_lists_url_additions

@dag(
    schedule=None,
    start_date=datetime.datetime.now(),
    catchup=False,
    tags=["netflix","country"],
)
def netflix_weekly_cntry():
    @task
    def get_batched_countries():
        '''
        Divide the Regions into batches of 15
        '''
        countries_to_search = list(countries.keys())
        return [countries_to_search[i:i+15] for i in range(0,len(countries_to_search),15)]
    
    @task(task_id="fetch_ntfx_page",pool="test_pool")
    def fetch_ntfx_pages(countries:str,media_type:str):
        '''
        Fetch the media_type list on the netflix page  
        '''
        docs = []
        for country in countries:
            ntfx_obj = NetflixPage(geography=country,media_type=media_type)
            docs.append(ntfx_obj.get_dict_obj())
        return docs

    @task(task_id='insert_docs_into_db')
    def insert_docs_into_db(ntfx_obj_docs:list[dict]):
        '''
        Insert list of documents in the database
        '''
        mongo_client = MongoDBClient(
            username = mongo_db_credentials['username'],
            password = mongo_db_credentials['password'],
            ip_add = mongo_db_credentials['ip'],
            port = mongo_db_credentials['port']
            )
        ids = mongo_client.insert('Trending_On_Netflix','Weekly', ntfx_obj_docs)
        
        print(ids,flush = True)
    
    @task(task_id='collect_docs')
    def collect_docs(list_docs):
        '''
        Collate the documents into a list
        '''
        docs = []
        for ld in list_docs:
            docs += ld
        return docs
    
    cntry_media_type = list(country_lists_url_additions.values())

    run_this_first = EmptyOperator(task_id="start_global_workflow")
    countries_to_search = get_batched_countries()
    fetched = fetch_ntfx_pages.expand(countries=countries_to_search,media_type=cntry_media_type)
    docs = collect_docs(fetched)

    run_this_first >> countries_to_search >> fetched >> docs >> insert_docs_into_db(docs)

netflix_weekly_cntry()
        

