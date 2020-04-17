from flask import Blueprint

# Creating a flask blueprint to integrate the templates and static folder
# This creates a blueprint named "elasticsearch_plugin" defined in the file __name__. The template folder is ../templates and static_folder is static
ElasticsearchBlueprint = Blueprint('elasticsearch', __name__, template_folder='../templates', static_folder='static', static_url_path='/static/')
