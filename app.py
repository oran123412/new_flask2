from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from textblob import TextBlob
import os

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://flask:password@127.0.0.1/flask'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)
    motivation = db.Column(db.String(500))

with app.app_context():
    db.create_all()

@app.route('/', methods=["GET"])
def index():
    t = Todo.query.all()
    return render_template("index.html", list_todo=t)

@app.route('/add', methods=["POST"])
def add():
    title = request.form.get("title")
    if not title:
        return redirect(url_for("index"))


    blob = TextBlob(title)
    sentiment = blob.sentiment.polarity 
    

    if sentiment > 0.3:
        motivation_text = "נשמע כמו משימה חיובית! תמשיך עם האנרגיה הזו 🌟"
    elif sentiment < -0.1:
        motivation_text = "זו נראית משימה מאתגרת, אבל קטן עליך! 💪"
    elif len(title) > 20:
        motivation_text = "וואו, זו משימה מפורטת. בוא נפרק אותה לצעדים קטנים 🧩"
    else:
        motivation_text = "עוד צעד בדרך ליעד שלך. קדימה! 🚀"

    new_todo = Todo(title=title, complete=False, motivation=motivation_text)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route('/update/<int:todo_id>')
def update(todo_id):
    todo = Todo.query.get(todo_id)
    if todo:
        todo.complete = not todo.complete
        db.session.commit()
    return redirect(url_for("index"))

@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    todo = Todo.query.get(todo_id)
    if todo:
        db.session.delete(todo)
        db.session.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
