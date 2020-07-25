# Service to build pipelines for ingesting, quering, visualizing, transforming and updating data.

![Service Design](data_pipeline.png)

* OS dependencies:
```bash
$: sudo apt-get install rabbitmq-server
```

* Python dependencies:
```bash
$: cd 
$: sudo pip install -r requirements.txt
```

* Init AWS engine
```bash
$: cat ~/.aws/credentials
[default]
aws_access_key_id = <aws_access_key_id>
aws_secret_access_key = <aws_secret_access_key>
region = us-west-2
```
## Create tables in DynamoDB and in Postgre
### 
```bash
$: cd data_pipeline_processor/data_workflow_api
$: python3 init_engine_aws.py
$: python3 init_engine_postgre.py
```
## Ingest data

* Run celery:
```bash
$: cd data_pipeline_processor/data_workflow_api
$: celery -A celery_tasks worker --loglevel=info
```
* Run tasks
```bash
$: cd data_pipeline_processor/data_workflow_api
$: 
```
* Monitor workers with [flower](https://flower.readthedocs.io/en/latest/)

```bash
$: cd data_pipeline_processor/data_workflow_api
$: celery -A celery_tasks flower --port=5555
```

## Query data and save results to a folder

```bash
$: cd data_pipeline_processor/query_service/
$: celery -A query_celery_tasks worker --loglevel=info
```

...
## Transform data
...
## Service performance
...
## Further considerations