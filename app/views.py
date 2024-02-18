from flask import Flask, render_template, redirect, url_for, request, session, abort, flash

from app import app

@app.route('/')
def index():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/add')
def add():
    return render_template("add.html")


