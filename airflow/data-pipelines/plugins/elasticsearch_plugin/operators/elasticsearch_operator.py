import json
import MySQLdb
from airflow.models import BaseOperator
from psycopg2.extras import RealDictCursor

from airflow.hooks.mysql_hook import MySqlHook
from airflow.utils.decorators import apply_defaults

from elasticsearch_plugin.hooks.elasticsearch_hook import ElasticsearchHook

class MySqlToElasticsearchTransfer(BaseOperator):
	"""
	Moves data from MySQL to Elasticsearch.
	In order to avoid the airflow worker to load all the data retrived from the PostgreSQL query into memory,
	we use server side cursor and fetch the rows using batches.
	
	:param sql: SQL query to execute against MySQL.
	:type sql: str

	:param index: Index where to save the data into Elasticsearch
	:type index: str

	:param mysql_conn_id: source MySQL connection
	:type mysql_conn_id: str

	:param elasticsearch_conn_id: source Elasticsearch connection
	:type elasticsearch_conn_id: str
	"""
	
	@apply_defaults
	def __init__(self, sql, index, mysql_conn_id='mysql_default', elasticsearch_conn_id='elasticsearch_default', *args, **kwargs):
		super(MySqlToElasticsearchTransfer, self).__init__(*args, **kwargs)
		self.sql 			= sql
		self.index			= index
		self.mysql_conn_id 		= mysql_conn_id
		self.elasticsearch_conn_id 	= elasticsearch_conn_id

	def execute(self, context):
		mysql 	    = MySqlHook(mysql_conn_id=self.mysql_conn_id).get_conn()
		es		    = ElasticsearchHook(elasticsearch_conn_id=self.elasticsearch_conn_id)

		self.log.info("Extracting data from MySQL: %s", self.sql)

		with MySQLdb.cursors.DictCursor(mysql) as mysql_cursor:
			mysql_cursor.execute(self.sql)
			for row in mysql_cursor:
				doc = json.dumps(row, indent=2)
				es.add_doc(index=self.index, doc_type='external', doc=doc)