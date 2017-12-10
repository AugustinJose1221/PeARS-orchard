# Import flask and template operators
from flask import Flask, render_template

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

# Sample HTTP error handling
#@app.errorhandler(404)
#def not_found(error):
#    return render_template('404.html'), 404

# Import a module / component using its blueprint handler variable (mod_auth)
from app.indexer.controllers import indexer as indexer_module
from app.api.controllers import api as api_module
from app.search.controllers import search as search_module
from app.pod_finder.controllers import pod_finder as pod_finder_module

# Register blueprint(s)
app.register_blueprint(indexer_module)
app.register_blueprint(api_module)
app.register_blueprint(search_module)
app.register_blueprint(pod_finder_module)
# ..

# Build the database:
# This will create the database file using SQLAlchemy
#db.drop_all()
db.create_all()


#Record Pod0 in case it is not registered
from app.api.models import KnownPods
if KnownPods.query.filter(KnownPods.url == "http://www.openmeaning.org/pod0/").first() == None:
    p = KnownPods(url="http://www.openmeaning.org/pod0/")
    p.description = "Pod0, the original English pod."
    db.session.add(p)
    db.session.commit()
    
