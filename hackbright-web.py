from flask import Flask, request, render_template
from flask.ext.sqlalchemy import SQLAlchemy

import hackbright

db = SQLAlchemy()

def connect_to_db(app):
    """Connects to database."""


    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///hackbrightdb'
    db.app = app
    db.init_app(app)

app = Flask(__name__)
connect_to_db(app)


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github', 'jhacks')
    first, last, github = hackbright.get_student_by_github(github)
    html = render_template("student_info.html",
                           first=first,
                           last=last,
                           github=github)
    return html


@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template("student_search.html")    


@app.route("/student-add", methods=['POST'])
def student_add():
    """Add a student."""

    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    github = request.form.get('github')

    QUERY = """INSERT INTO students VALUES (:first_name, :last_name, :github)"""

    db.session.execute(QUERY, {'first_name': first_name, 'last_name': last_name, 'github': github})

    db.session.commit()

    return render_template("student_added.html", first_name=first_name, last_name=last_name) 


@app.route("/student-creation")
def student_creation():
    """Form for student creation"""

    return render_template("student_add.html")    


if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
