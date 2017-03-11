import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from flask_cors import CORS, cross_origin

app = Flask(__name__) # create the application instance
app.config.from_object(__name__) # load config from this file , capture.py

# Load default config and override config from an environment variable
app.config.update(dict(
	DATABASE=os.path.join(app.root_path, 'capture.db'),
	SECRET_KEY='development key',
	USERNAME='admin',
	PASSWORD='default'
))
app.config.from_envvar('CAPTURE_SETTINGS', silent=True)

CORS(app)

def connect_db():
	"""Connects to the specific database."""
	rv = sqlite3.connect(app.config['DATABASE'])
	rv.row_factory = sqlite3.Row
	return rv

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')

@app.route("/capture", methods=['POST'])
def add_entry():
	db = get_db()
	print "This is the title: %s" % request.form['text']
	db.execute('insert into entries (title, text, url) values (?, ?, ?)',
					[request.form['title'], request.form['text'], request.form['url']])
	db.commit()
	flash('New entry was successfully posted')
	return '', 201

@app.route("/entries", methods=['GET'])
def get_entries():
	db = get_db()
	cur = db.execute('select title, text, url from entries order by id desc')
	entries = cur.fetchall()
	print entries
	return '', 201