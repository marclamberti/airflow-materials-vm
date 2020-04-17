import json
from airflow.models import BaseOperator
from psycopg2.extras import RealDictCursor

from airflow.hooks.postgres_hook import PostgresHook
from airflow.utils.decorators import apply_defaults

from elasticsearch_plugin.hooks.elasticsearch_hook import ElasticsearchHook

class PostgresToElasticsearchTransfer(BaseOperator):
	"""
	Moves data from PostgreSQL to Elasticsearch.
	In order to avoid the airflow worker to load all the data retrived from the PostgreSQL query into memory,
	we use server side cursor and fetch the rows using batches.
	
	:param sql: SQL query to execute against PostgreSQL.
	:type sql: str

	:param index: Index where to save the data into Elasticsearch
	:type index: str

	:param postgres_conn_id: source PostgreSQL connection
	:type postgres_conn_id: str

	:param elasticsearch_conn_id: source Elasticsearch connection
	:type elasticsearch_conn_id: str
	"""
	
	@apply_defaults
	def __init__(self, sql, index, postgres_conn_id='postgres_default', elasticsearch_conn_id='elasticsearch_default', *args, **kwargs):
		super(PostgresToElasticsearchTransfer, self).__init__(*args, **kwargs)
		self.sql 			= sql
		self.index			= index
		self.postgres_conn_id 		= postgres_conn_id
		self.elasticsearch_conn_id 	= elasticsearch_conn_id

	def execute(self, context):
		postgres 	= PostgresHook(postgres_conn_id=self.postgres_conn_id).get_conn()
		es		= ElasticsearchHook(elasticsearch_conn_id=self.elasticsearch_conn_id)

		self.log.info("Extracting data from PostgreSQL: %s", self.sql)

		with postgres.cursor(name="serverCursor", cursor_factory=RealDictCursor) as postgres_cursor:
			postgres_cursor.itersize=2000
			postgres_cursor.execute(self.sql)
			for row in postgres_cursor:
				doc = json.dumps(row, indent=2)
				es.add_doc(index=self.index, doc_type='external', doc=doc)
		postgres.close()
