from flask import Flask, render_template, request, redirect, send_file
import sqlite3
import pandas as pd
import subprocess
import os

application = Flask(__name__)

# Connexion DB
def connect_db():
    return sqlite3.connect("database.db")

# Création table
def init_db():
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS survey (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        age INTEGER,
        sexe TEXT,
        universite TEXT,
        budget REAL,
        temps_online REAL,
        operateur TEXT,
        usage TEXT
    )
    """)
    
    conn.commit()
    conn.close()

@application.route("/")
def index():
    return render_template("form.html")

@application.route("/submit", methods=["POST"])
def submit():
    data = (
        request.form["age"],
        request.form["sexe"],
        request.form["universite"],
        request.form["budget"],
        request.form["temps"],
        request.form["operateur"],
        request.form["usage"]
    )
    
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("""
    INSERT INTO survey (age, sexe, universite, budget, temps_online, operateur, usage)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, data)
    
    conn.commit()
    conn.close()
    
    return redirect("/")

@application.route("/export")
def export():
    conn = connect_db()
    df = pd.read_sql_query("SELECT age, sexe, universite, budget, temps_online, operateur, usage FROM survey", conn)
    df.to_csv("data/export.csv", index=False)
    conn.close()
    
    return "Export terminé !"

@application.route("/show-analysis")
def show():
    subprocess.run(["Rscript", "analyse.R"])
    return send_file("Rplots.pdf")


@application.route("/download-analysis")
def download_analysis():
    subprocess.run(["Rscript", "analyse.R"])
    return send_file("Rplots.pdf", as_attachment=True, download_name="mon-rapport-analyse.pdf")
    
if __name__ == "__main__":
    init_db()
    application.run(debug=True)    

