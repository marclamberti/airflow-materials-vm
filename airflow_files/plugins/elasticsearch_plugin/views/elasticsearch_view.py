from flask_admin import BaseView, expose
from elasticsearch_plugin.hooks.elasticsearch_hook import ElasticsearchHook

class ElasticsearchView(BaseView):
	@expose('/', methods=['GET', 'POST'])
	def index(self):
		try:
			es = ElasticsearchHook()
			data = es.info()
			isup = es.ping()
		except:
			data = {}
			isup = False
		return self.render("elasticsearch_plugin.html", data=data, isup=isup)
