from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import psycopg2

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://jem:flanagan@localhost:5432/feh1'
app.debug = True
db = SQLAlchemy(app)
db.Model.metadata.reflect(db.engine)


class Cd3Data(db.Model):
    __table__ = db.Model.metadata.tables['cd3_data']

    def __repr__(self):
        return self.stationnum

if __name__ == '__main__':
    app.run()
