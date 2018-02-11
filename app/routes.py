from app import app
import flask

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Kristian'}
    return flask.render_template('index.html', title='Home', user=user)