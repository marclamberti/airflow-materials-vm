from airflow.hooks.base_hook import BaseHook
from airflow.utils.log.logging_mixin import LoggingMixin
from ssl import create_default_context

from elasticsearch import Elasticsearch

class ElasticsearchHook(BaseHook, LoggingMixin):
	"""
	Hook used to interact with Elasticsearch

	
	"""
	def __init__(self, elasticsearch_conn_id='elasticsearch_default'):
		conn = self.get_connection(elasticsearch_conn_id)
		
		conn_config = {}
		hosts = []

		if conn.host:
			hosts = conn.host.split(',')
		if conn.port:
			conn_config['port'] = int(conn.port)
		if conn.login:
			conn_config['http_auth'] = (conn.login, conn.password)

		conn_config['scheme'] = conn.extra_dejson.get('scheme', 'http')
		
		ssl_cert_path = conn.extra_dejson.get('cert_path', None)
		if ssl_cert_path:
			conn_config['ssl_context'] = create_default_context(cafile=ssl_cert_path)
		
		verify_certs = conn.extra_dejson.get('verify_certs', None)
		if verify_certs:
			conn_config['verify_certs'] = verify_certs

		conn_config['sniff_on_start'] = conn.extra_dejson.get('sniff_on_start', False)

		self.es 	= Elasticsearch(hosts, **conn_config)
		self.index 	= conn.schema

	def get_conn(self):
		return self.es

	def get_index(self):
		return self.index

	def set_index(self, index):
		self.index = index

	def search(self, index, body):
		self.set_index(index)
		res = self.es.search(index=self.index, body=body)
		return res

	def create_index(self, index, body):
		self.set_index(index)
		res = self.es.indices.create(index=self.index, body=body)
		return res

	def add_doc(self, index, doc_type, doc):
		self.set_index(index)
		res = self.es.index(index=index, doc_type=doc_type, body=doc)
		return res
	
	def info(self):
		return self.es.info()

	def ping(self):
		return self.es.ping()
