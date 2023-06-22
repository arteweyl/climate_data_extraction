curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.6.2/docker-compose.yaml'
mkdir -p ./dags ./logs ./plugins ./config ./env_exchange
echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env
