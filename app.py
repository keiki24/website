import flask
import setting

# Views
from main import Main
from login import Login
from remote import Remote
from music import Music

app = flask.Flask(__name__)
app.secret_key = setting.secret_key

# Routes
app.add_url_rule('/', 
				 view_func=Main.as_view('login')
				 methods=["GET", "POST"])
app.add_url_rule('/login/', 
				  view_func=Login.as_view('login')
				  methods=["GET", "POST"])
app.add_url_rule('/remote/',
				  view_func=Login.as_view('remote')
				  methods=['GET', "POST"])
