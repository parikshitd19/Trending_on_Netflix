from airflow.decorators import dag, task
from airflow.operators.empty import EmptyOperator
# from airflow.utils.trigger_rule import TriggerRule
import datetime

from trending_on_netflix.netflix_page import NetflixPage
from trending_on_netflix.database.mongodb_client import MongoDBClient
from trending_on_netflix.config import mongo_db_credentials, countries, country_lists_url_additions, global_lists_url_additions


@dag(
    schedule=None,
    start_date=datetime.datetime.now(),
    catchup=False,
    tags=["batch-insert", "parallel", "celery", "all data"],
)
def netflix_weekly_global_dag():
    
    @task(task_id="fetch_ntfx_page")
    def fetch_ntfx_page(media_type:str):
        '''
        Fetch the media_type list on the netflix page  
        '''
        ntfx_obj = NetflixPage(media_type=media_type)
        return ntfx_obj.get_dict_obj()
    
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
    def collect_docs(docs):
        '''
        Collate the documents into a list
        '''
        return list(docs)
    
   
    media_types = list(global_lists_url_additions.values())

    run_this_first = EmptyOperator(task_id="start_workflow")
    fetched = fetch_ntfx_page.expand(media_type=media_types)
    docs = collect_docs(fetched)
    

    run_this_first >> fetched >> docs >> insert_docs_into_db(docs)

netflix_weekly_global_dag()
