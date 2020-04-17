from airflow.plugins_manager import AirflowPlugin

from elasticsearch_plugin.hooks.elasticsearch_hook import ElasticsearchHook

# Views / Blueprints / MenuLinks are instantied objects
class ElasticsearchPlugin(AirflowPlugin):
	name 			= "elasticsearch_plugin"
	operators 		= []
	sensors			= []
	hooks			= [ ElasticsearchHook ]
	executors		= []
	admin_views		= []
	flask_blueprints	= []
	menu_links		= []

