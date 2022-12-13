from flask import Flask, render_template, request
import mysql.connector
from datetime import date
app = Flask(__name__)

mydb = mysql.connector.connect(
        host="localhost",
        user="utente",
        password="1",
        database="recensioni"
    )

mycursor = mydb.cursor()

@app.route("/")
def main():
    
    mycursor.execute("SELECT COUNT(*) FROM reviews")

    myresult = mycursor.fetchall()
    
    return render_template('index.html', count=myresult[0][0])

@app.route('/submitReview', methods=['POST'])
def insert():
        

    sql = "INSERT INTO reviews (productName, userName, postDate, text, rating, likeCount, dislikeCount) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (request.form.get("productName"), request.form.get("username"), date.today().strftime("%Y-%m-%d"), request.form.get("reviewText"), request.form.get("rating"), 0, 0)
    mycursor.execute(sql, val)
    
    mydb.commit()
    
    print(mycursor.rowcount, "record inserted.")
    return 'OSSI'

@app.route("/fetchReview", methods=['GET'])
def fetchReview():
    rowCount = request.args.get("rowCount")
    startRow = request.args.get("startRow")
    mycursor.execute("SELECT * FROM reviews WHERE id>=" + startRow +" LIMIT " + rowCount)
    myresult = mycursor.fetchall()
    print(rowCount)
    return myresult
