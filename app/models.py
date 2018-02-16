from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_has = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Stat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True)
    session = db.Column(db.Integer, index=True)

    def __repr__(self):
        return '<Stat Datetime{}, session{}>'.format(self.timestamp, self.session)
