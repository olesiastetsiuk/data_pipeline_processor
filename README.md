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
## Ingest data
...
## Query data
...
## Transform data
...
## Service performance
...
## Further considerations