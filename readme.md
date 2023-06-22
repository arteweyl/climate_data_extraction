1 -  just run chmod 777 config.bash to execute this bash command, it will create for you the needed enviroment and download the docker image.

2 -  add on the docker-compose the path ${AIRFLOW_PROJ_DIR:-.}/env_exchange:/opt/airflow/env_exchange

test and make your mods, and enjoy :)
