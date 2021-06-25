#naredba za instalaciju flaska
#pip install -r requierments.txt


import os
from flask import Flask, render_template, request, redirect, url_for
from sqla_wrapper import SQLAlchemy #uvoz sql-wrappera iz requiermentsa

app = Flask(__name__)

#db = SQLAlchemy("sqlite:///db.sqlite") #konekcija na bazu podatka --> na 1:08 zakomentirano da bi se sačuvala verzija kod zbog uploadanja na heroku

db_url = os.getenv("DATABASE_URL", "sqlite:///db.sqlite").replace("postgres://", "postgresql://", 1)
db = SQLAlchemy(db_url)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True) #primarni ključ, pomoću njega označavamo redove u bazi podataka
    author = db.Column(db.String, unique=False)
    text = db.Column(db.String, unique=False)

db.create_all()

@app.route("/", methods=["GET"])#početna stranica, dodaje se metoda get ba 53:22
def index():

    messages = db.query(Message).all() #spremanje svega iz baze i ispisivanje na glavnu stranicu

    return render_template("index.html", messages=messages) #dodano na 56:32 messages kako bi se mogla prikazati lista

@app.route("/add-message", methods=["POST"])
def add_message():
    username = request.form.get("username")
    text = request.form.get("text")

    print("{0}: {1}".format(username, text))

    message = Message(author=username, text=text)
    message.save()

    return redirect("/") #redirektanje korisnika na rutu koju želimo
if __name__ == "__main__":
    app.run()