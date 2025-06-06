# Trending on Netflix
In this repository I have created a data scraping framework to extract weekly top 10 list available on [Netflix's website](https://www.netflix.com/tudum/top10).


## Running dags on Apache Airflow deployed using Docker
To run a dag utilising the code follow the following steps:
- Run Apache Airflow using Docker Compose. The following should be the folder structure.
```
Apache Airflow
|---config
|---dags
|---logs
|---plugins
|---Trending_on_Netflix
    |---trending_on_netflix
        |---database
        |---bsoup.py
        |---config.py
        |---helper_functions.py
        |---netflix_page.py
    |---setup.py
    |---dags
        |----dag_file_1.py
        |----dag_file_2.py
        |----...
        |----...
    |---README.md
    |---.github
|---docker-compose.yaml
|---Dockerfile
```
- Inside the [config.py](trending_on_netflix/config.py) add the appropriate values:
```
mongo_db_credentials = {
    'ip':<ip-address>,
    'port':<port>,
    'username':<username>,
    'password':<password>
}
```
- In the mongodb instance ensure there is a database ```Trending_On_Netflix``` and collection ```Weekly```
- In the Docker file ensure the following lines are there. Make sure to replace <dag_file> with the name of file you are trying to run:
```
USER root
COPY Trending_on_Netflix /opt/airflow/Trending_on_Netflix
RUN chown -R airflow: /opt/airflow/Trending_on_Netflix

USER airflow
RUN cp /opt/airflow/Trending_on_Netflix/dags/<dag_file>.py /opt/airflow/dags
RUN pip install /opt/airflow/Trending_on_Netflix
```
