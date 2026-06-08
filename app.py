from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="tiger",
    database="studentdb"
)

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():

    username = request.form["userid"]
    password = request.form["passwordid"]

    cursor = db.cursor(buffered=True)

    query = "SELECT * FROM users WHERE BINARY username=%s AND BINARY password=%s"

    cursor.execute(query, (username, password))

    user = cursor.fetchone()

    cursor.close()

    if user:
        return render_template("success.html")
    else:
        return render_template("failure.html")
    


    
@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/savestudent", methods=["POST"])
def savestudent():

    name = request.form["student_name"]
    age = request.form["student_age"]
    college = request.form["student_college"]
    phone = request.form["student_phone"]
    branch = request.form["student_branch"]
    password = request.form["password"]

    cursor = db.cursor()

    
    # studentdetails table
    cursor.execute(
        """
        INSERT INTO studentdetails
        (student_name,student_age,student_college,student_phone,student_branch,password)
        VALUES(%s,%s,%s,%s,%s,%s)
        """,
        (name,age,college,phone,branch,password)
    )

    db.commit()

    cursor.close()

    return "Student Registered Successfully"

@app.route("/getstudents")
def getstudents():

    cursor = db.cursor()

    cursor.execute("SELECT * FROM studentdetails")

    students = cursor.fetchall()

    cursor.close()

    return render_template("students.html", students=students)


@app.route("/findstudent")
def findstudent():
    return render_template("findstudent.html")


@app.route("/searchstudent", methods=["POST"])
def searchstudent():

    student_id = request.form["student_id"]

    cursor = db.cursor()

    query = """
    SELECT * FROM studentdetails
    WHERE student_id=%s
    """

    cursor.execute(query, (student_id,))

    student = cursor.fetchone()

    cursor.close()

    return render_template(
        "studentresult.html",
        student=student
    )

@app.route("/logout")
def logout():
    return redirect("/")

@app.route("/dashboard")
def dashboard():
    return render_template("success.html")


if __name__ == "__main__":
    app.run(debug=True)