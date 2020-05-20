import os
import datetime
import sqlite3

from flask import Flask, g, flash, render_template
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import Regexp

SECRET = os.environ["SECRET"]
db = os.environ["DB"]
title = db.split(".")[0]

def get_conn():
    conn = getattr(g, "_database", None)
    if conn is None:
        conn = g._database = sqlite3.connect(db)
    return conn

def add_tag(conn, tag):
    with conn:
        conn.execute("INSERT INTO tags(tag_id, insert_time) VALUES(?, ?);", (tag, datetime.datetime.now()))

def get_tags(conn):
    c = conn.cursor()
    c.execute("SELECT tag_id, insert_time FROM tags ORDER BY tag_id;")
    return [dict(zip(("tag", "time"), row)) for row in c.fetchall()]

class TagForm(FlaskForm):
    tag = StringField("Bag Tag", validators=[Regexp("^[0-9]{4}$")])


app = Flask(__name__)
app.secret_key = SECRET

@app.teardown_appcontext
def teardown_conn(exception):
    conn = getattr(g, "_database", None)
    if conn is not None:
        conn.close()

@app.route("/", methods=("GET",))
def index():
    form = TagForm()
    return render_template("index.html", title=title, form=form)

@app.route("/", methods=("POST",))
def submit():
    form = TagForm()
    if not form.validate_on_submit():
        flash(f"Invalid Bag Tag \"{form.tag.data}\"", "error")
        return render_template("index.html", title=title, form=form)

    try:
        add_tag(get_conn(), form.tag.data)
        flash(f"Bag Tag {form.tag.data} added")
        form.tag.data = ""
    except sqlite3.IntegrityError:
        flash(f"Bag Tag {form.tag.data} has already been added", "error")

    return render_template("index.html", title=title, form=form)

@app.route("/tags")
def tags():
    return render_template("tags.html", tags=get_tags(get_conn()))
