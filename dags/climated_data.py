"""extract climate data from visual crossing API
This dag works inside a docker image, but I configured a env_exchange paste in docker-compose file to read/write data.
 in this paste you will need to have a.env file for with your api_key from visual crossing"""

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
import pendulum
import os
from dotenv import load_dotenv
from pathlib import Path
from os.path import join
import pandas as pd
from airflow.macros import ds_add


def extract_data(data_interval_end):

    
    load_dotenv(dotenv_path=Path("/opt/airflow/env_exchange/.env"))

    city = 'Belem'
    key = os.environ.get("API_KEY")

    URL = join('https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/',
                f'{city}/{data_interval_end}/{ds_add(data_interval_end,7)}?unitGroup=metric&include=days&key={key}&contentType=csv')
    df = pd.read_csv(URL)
    file_path = f'/opt/airflow/used_paste/data_pipeline/weeks/week={data_interval_end}/'
    df.to_csv(file_path + 'raw_data.csv')
    df[['datetime', 'tempmin', 'temp', 'tempmax']].to_csv(file_path + 'temperatures.csv')
    df[['datetime', 'description', 'icon']].to_csv(file_path + 'conditions.csv')


with DAG(
        "dados_climaticos",
        start_date=pendulum.datetime(2022, 7, 22, tz="UTC"),
        schedule_interval='0 0 * * 1', # executes every monday
) as dag:
    task_1 = BashOperator(
        task_id = 'make_paste',
        bash_command='mkdir /opt/airflow/used_paste/data_pipeline/weeks/week={{data_interval_end.strftime("%Y-%m-%d")}}'
    )
    task_2 = PythonOperator(
        task_id = 'extract_data',
        python_callable = extract_data,
        op_kwargs = {'data_interval_end': '{{data_interval_end.strftime("%Y-%m-%d")}}'}
    )

task_1 >> task_2