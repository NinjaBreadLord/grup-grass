"""control dependencies to support CRUD app routes and APIs"""
from flask import Blueprint, render_template, request, url_for, redirect, jsonify, make_response
from flask_login import login_required

from krug.query import *
from model import Students
# blueprint defaults https://flask.palletsprojects.com/en/2.0.x/api/#blueprint-objects
app_krug = Blueprint('krug', __name__,
                     url_prefix='/krug',
                     template_folder='templates/kruggy/',
                     static_folder='static',
                     static_url_path='static')

""" Blueprint is established to isolate Application control code for CRUD operations, key features:
    1.) 'Users' table control methods, controls relationship between User Actions and Database Model
    2.) Control methods are achieved using app routes for each CRUD operations
    3.) login required to restrict CRUD operations to identified users
"""


# Default URL for Blueprint
@app_krug.route('/')
def crud():
    """obtains all Users from table and loads Admin Form"""
    return render_template("krugg.html", table=students_all())


# Flask-Login directs unauthorised users to this unauthorized_handler


# CRUD create/add
@app_krug.route('/create/', methods=["POST"])
def create():
    """gets data from form and add it to Users table"""
    if request.form:
        po = Students(
            request.form.get("studentID"),
            request.form.get("Text"),
        )
        po.create()
    return redirect(url_for('krug.crud'))


# CRUD read
@app_krug.route('/read/', methods=["POST"])
def read():
    """gets userid from form and obtains corresponding data from Users table"""
    table = []
    if request.form:
        studentid = request.form.get("studentid")
        po = student_by_id(studentid)
        if po is not None:
            table = [po.read()]  # placed in list for easier/consistent use within HTML
    return render_template("krugg.html", table=table)


# CRUD update
@app_krug.route('/update/', methods=["POST"])
def update():
    """gets userid and name from form and filters and then data in  Users table"""
    if request.form:
        studentid = request.form.get("studentid")
        firstname = request.form.get("firstname")
        po = student_by_id(studentid)
        if po is not None:
            po.update(firstname)
    return redirect(url_for('krug.crud'))


# CRUD delete
@app_krug.route('/delete/', methods=["POST"])
def delete():
    """gets userid from form delete corresponding record from Users table"""
    if request.form:
        studentid = request.form.get("studentid")
        po = student_by_id(studentid)
        if po is not None:
            po.delete()
    return redirect(url_for('krug.crud'))


# Search Form
@app_krug.route('/search/')
def search():
    """loads form to search Users data"""
    return render_template("search.html")


# Search request and response
@app_krug.route('/search/term/', methods=["POST"])
def search_term():
    """ obtain term/search request """
    req = request.get_json()
    term = req['term']
    response = make_response(jsonify(students_ilike(term)), 200)
    return response
