import flask
import datetime
from app.forms import LoginForm
from config import Config

app = flask.Flask(__name__)
app.config.from_object(Config)


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


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flask.flash('Login requested for user {}, remember me ={}'.format(
            form.username.data, form.remember_me.data
        ))
        return flask.redirect(flask.url_for('index'))
    return flask.render_template('login.html', title='Sign In', form=form)


if __name__ == '__main__':
    app.run()
