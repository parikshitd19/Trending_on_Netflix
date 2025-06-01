# Trending on Netflix
In this repository I have created a data scraping framework to extract weekly top 10 list availble on [Netflix's website](https://www.netflix.com/tudum/top10).

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
    |---setup.py
    |---dag_file.py
    |---README.md
    |---.github
|---docker-compose.yaml
|---Dockerfile
```
- In the Docker file ensure the following lines are there. Make sure to replace dag_file with the name of file you are trying to run:
```
USER root
COPY Trending_on_Netflix /opt/airflow/Trending_on_Netflix
RUN chown -R airflow: /opt/airflow/Trending_on_Netflix

USER airflow
RUN cp /opt/airflow/Trending_on_Netflix/dag_file.py /opt/airflow/dags
RUN pip install /opt/airflow/Trending_on_Netflix


```
