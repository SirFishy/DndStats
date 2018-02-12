import flask
import datetime

app = flask.Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    today = datetime.date.today()
    user = {'username': 'Kristian'}
    stats = [
        {
            'date': {'date': today, 'displaydate': today.strftime("%A %d. %B %Y")},
            'session': '1'
        },
        {
            'date': {'date': today, 'displaydate': today.strftime("%A %d. %B %Y")},
            'session': '1'
        }
    ]
    return flask.render_template('index.html', title='Home', user=user, stats=stats)


if __name__ == '__main__':
    app.run()
