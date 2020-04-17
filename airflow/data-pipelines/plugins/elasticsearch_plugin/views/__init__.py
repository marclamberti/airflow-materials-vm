from elasticsearch_plugin.views.elasticsearch_view import ElasticsearchView

# By leaving empty the parameter "category" you will get a direct to link to your view. (no drop down menu) 
ELASTICSEARCH_PLUGIN_VIEWS = [
	ElasticsearchView(category='Elasticsearch Plugin', name='Elasticsearch Dashboard')	
]
