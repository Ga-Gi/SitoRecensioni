from flask import Flask, render_template, request
import mysql.connector
from datetime import date
app = Flask(__name__)

@app.route("/")
def main():
    return render_template('index.html')

@app.route('/submitReview', methods=['POST'])
def insert():
    mydb = mysql.connector.connect(
        host="localhost",
        user="utente",
        password="1",
        database="recensioni"
    )

    mycursor = mydb.cursor()    

    sql = "INSERT INTO reviews (productName, userName, postDate, text, rating, likeCount, dislikeCount) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (request.form.get("productName"), request.form.get("username"), date.today().strftime("%Y-%m-%d"), request.form.get("reviewText"), request.form.get("rating"), 0, 0)
    mycursor.execute(sql, val)
    
    mydb.commit()
    
    print(mycursor.rowcount, "record inserted.")
    return 'OSSI'