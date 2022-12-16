from flask import Flask, render_template, request, send_from_directory
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
    return '<script>window.location.href="/"</script>'

@app.route("/fetchReview", methods=['GET'])
def fetchReview():
    rowCount = request.args.get("rowCount")
    startRow = request.args.get("startRow")
    mycursor.execute("SELECT * FROM reviews WHERE id>=" + startRow +" LIMIT " + rowCount)
    myresult = mycursor.fetchall()
    return myresult

@app.route("/changeLike", methods=['GET'])
def changeLike():
    if (request.args.get("increment") == "true"):
        mycursor.execute("UPDATE reviews SET likeCount = likeCount + 1 WHERE id=" + request.args.get("id"))
    else:
        mycursor.execute("UPDATE reviews SET likeCount = IF(likeCount>0, likeCount - 1, likeCount) WHERE id=" + request.args.get("id"))
    mydb.commit()
    return request.args.get("increment")

@app.route("/changeDislike", methods=['GET'])
def changeDislike():
    if (request.args.get("increment") == "true"):
        mycursor.execute("UPDATE reviews SET dislikeCount = dislikeCount + 1 WHERE id=" + request.args.get("id"))
    else:
        mycursor.execute("UPDATE reviews SET dislikeCount = IF(dislikeCount>0, dislikeCount - 1, dislikeCount)  WHERE id=" + request.args.get("id"))
    mydb.commit()
    return request.args.get("increment")


