from flask import Flask, render_template, request, redirect
import os
import mysql.connector

app = Flask(__name__)

mysql.connector.connect(
    host=" reseau.proxy.rlwy.net",
    user="root",
    password="pDxbDmrFEnZRkdlXKWCjAtixtSJkyHJA",
    database="studentdb",
    port=33159 
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

    return render_template("register_success.html")

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

    cursor = db.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM studentdetails"
    )

    total_students = cursor.fetchone()[0]

    cursor.close()

    return render_template(
        "success.html",
        total_students=total_students
    )

@app.route("/updatestudent")
def updatestudent():
    return render_template("updatestudent.html")


@app.route("/updaterecord", methods=["POST"])
def updaterecord():

    student_id = request.form["student_id"]
    name = request.form["student_name"]
    phone = request.form["student_phone"]

    cursor = db.cursor()

    cursor.execute(
    """
    UPDATE studentdetails
    SET student_name=%s,
        student_phone=%s
    WHERE student_id=%s
    """,
    (name, phone, student_id)
)
    db.commit()

    cursor.close()

    return render_template("update_success.html")

@app.route("/deletestudent")
def deletestudent():
    return render_template("deletestudent.html")


@app.route("/deleterecord", methods=["POST"])
def deleterecord():

    student_id = request.form["student_id"]

    cursor = db.cursor()

    cursor.execute(
        """
        DELETE FROM studentdetails
        WHERE student_id=%s
        """,
        (student_id,)
    )

    db.commit()

    cursor.close()

    return render_template("delete_success.html")

@app.route("/products")
def products():
    return render_template("products_dashboard.html")

@app.route("/addproduct")
def addproduct():
    return render_template("addproduct.html")

@app.route("/saveproduct", methods=["POST"])
def saveproduct():

    name = request.form["product_name"]
    price = request.form["product_price"]
    category = request.form["product_category"]
    quantity = request.form["product_quantity"]

    cursor = db.cursor()

    cursor.execute(
        """
        INSERT INTO products
        (product_name, product_price, product_category, product_quantity)
        VALUES(%s, %s, %s, %s)
        """,
        (name, price, category, quantity)
    )

    db.commit()
    cursor.close()

    return "Product Added Successfully"

@app.route("/getproducts")
def getproducts():

    cursor = db.cursor()

    cursor.execute("SELECT * FROM products")

    products = cursor.fetchall()

    cursor.close()

    return render_template(
        "products.html",
        products=products
    )

@app.route("/findproduct")
def findproduct():
    return render_template("findproduct.html")

@app.route("/searchproduct", methods=["POST"])
def searchproduct():

    product_id = request.form["product_id"]

    cursor = db.cursor()

    cursor.execute(
        """
        SELECT * FROM products
        WHERE product_id=%s
        """,
        (product_id,)
    )

    product = cursor.fetchone()

    cursor.close()

    return render_template(
        "productresult.html",
        product=product
    )

@app.route("/updateproduct")
def updateproduct():
    return render_template("updateproduct.html")

@app.route("/updateproductrecord", methods=["POST"])
def updateproductrecord():

    product_id = request.form["product_id"]
    price = request.form["product_price"]
    quantity = request.form["product_quantity"]

    cursor = db.cursor()

    cursor.execute(
        """
        UPDATE products
        SET product_price=%s,
            product_quantity=%s
        WHERE product_id=%s
        """,
        (price, quantity, product_id)
    )

    db.commit()
    cursor.close()

    return "Product Updated Successfully"
@app.route("/deleteproduct")
def deleteproduct():
    return render_template("deleteproduct.html")
@app.route("/deleteproductrecord", methods=["POST"])
def deleteproductrecord():

    product_id = request.form["product_id"]

    cursor = db.cursor()

    cursor.execute(
        """
        DELETE FROM products
        WHERE product_id=%s
        """,
        (product_id,)
    )

    db.commit()
    cursor.close()

    return "Product Deleted Successfully"
@app.route("/buyproduct")
def buyproduct():
    return render_template("buyproduct.html")

@app.route("/buyproductrecord", methods=["POST"])
def buyproductrecord():

    product_id = request.form["product_id"]
    buy_quantity = int(request.form["buy_quantity"])

    cursor = db.cursor()

    # Check stock
    cursor.execute(
        """
        SELECT product_name, product_price, product_quantity
        FROM products
        WHERE product_id=%s
        """,
        (product_id,)
    )

    product = cursor.fetchone()

    if product:

        product_name = product[0]
        product_price = float(product[1])
        current_quantity = int(product[2])


        if current_quantity >= buy_quantity:

            # Update stock
            new_quantity = current_quantity - buy_quantity

            cursor.execute(
                """
                UPDATE products
                SET product_quantity=%s
                WHERE product_id=%s
                """,
                (new_quantity, product_id)
            )

            # Calculate total price
            total_amount = product_price * buy_quantity

            # Save order
            cursor.execute(
                """
                INSERT INTO orders
                (product_id, product_name, quantity, total_price)
                VALUES(%s,%s,%s,%s)
                """,
                (
                    product_id,
                    product_name,
                    buy_quantity,
                    total_amount
                )
            )

            db.commit()

            message = "Product Purchased Successfully"

        else:

            message = "Insufficient Stock"

    else:

        message = "Product Not Found"

    cursor.close()

    return render_template(
        "purchase_success.html",
        message=message
    )

@app.route("/studentservices")
def studentservices():
    return render_template("student_services.html")

@app.route("/customershopping")
def customershopping():
    return render_template("customer_shopping.html")

@app.route("/reports")
def reports():

    cursor = db.cursor()

    # Count Students
    cursor.execute("SELECT COUNT(*) FROM studentdetails")
    total_students = cursor.fetchone()[0]

    # Count Products
    cursor.execute("SELECT COUNT(*) FROM products")
    total_products = cursor.fetchone()[0]

    cursor.close()

    return render_template(
        "reports.html",
        total_students=total_students,
        total_products=total_products
    )
@app.route("/storemanagement")
def storemanagement():
    return render_template("products_dashboard.html")

@app.route("/addtocart")
def addtocart():
    return render_template("addtocart.html")


@app.route("/viewcart")
def viewcart():

    cursor = db.cursor()

    cursor.execute("SELECT * FROM cart")

    cart_items = cursor.fetchall()

    cursor.close()

    return render_template(
        "viewcart.html",
        cart_items=cart_items
    )

@app.route("/vieworders")
def vieworders():

    cursor = db.cursor()

    cursor.execute("SELECT * FROM orders")

    orders = cursor.fetchall()

    cursor.close()

    return render_template(
        "vieworders.html",
        orders=orders
    )

@app.route("/addtocartrecord", methods=["POST"])
def addtocartrecord():

    product_id = request.form["product_id"]
    quantity = int(request.form["quantity"])

    cursor = db.cursor()

    # Get product details
    cursor.execute(
        """
        SELECT product_name, product_price
        FROM products
        WHERE product_id=%s
        """,
        (product_id,)
    )

    product = cursor.fetchone()

    if product:

        product_name = product[0]
        price = product[1]

        cursor.execute(
            """
            INSERT INTO cart
            (product_id, product_name, quantity, price)
            VALUES(%s,%s,%s,%s)
            """,
            (product_id, product_name, quantity, price)
        )

        db.commit()

        message = "Product Added To Cart Successfully"

    else:
        message = "Product Not Found"

    cursor.close()

    return render_template(
    "cart_success.html",
    message=message
)

   

@app.route("/blogdashboard")
def blogdashboard():
    return render_template("blog_dashboard.html")

@app.route("/addpost")
def addpost():
    return render_template("add_post.html")
@app.route("/savepost", methods=["POST"])
def savepost():

    title = request.form["title"]
    content = request.form["content"]
    author = request.form["author"]

    cursor = db.cursor()

    cursor.execute(
        """
        INSERT INTO blog_posts
        (title, content, author)
        VALUES(%s,%s,%s)
        """,
        (title, content, author)
    )

    db.commit()
    cursor.close()

    return render_template("post_success.html")

@app.route("/viewposts")
def viewposts():

    cursor = db.cursor()

    cursor.execute(
        "SELECT * FROM blog_posts"
    )

    posts = cursor.fetchall()

    cursor.close()

    return render_template(
        "view_posts.html",
        posts=posts
    )
@app.route("/postdetails/<int:post_id>")
def postdetails(post_id):

    cursor = db.cursor()

    # Get blog post
    cursor.execute(
        "SELECT * FROM blog_posts WHERE post_id=%s",
        (post_id,)
    )

    post = cursor.fetchone()

    # Get comments for this post
    cursor.execute(
        "SELECT * FROM comments WHERE post_id=%s",
        (post_id,)
    )

    comments = cursor.fetchall()
    cursor.execute("SELECT * FROM replies")
    replies = cursor.fetchall()
    cursor.close()
    return render_template(
    "post_details.html",
    post=post,
    comments=comments,
    replies=replies
)

@app.route("/updatepost")
def updatepost():
    return render_template("updatepost.html")

@app.route("/updatepostrecord", methods=["POST"])
def updatepostrecord():

    post_id = request.form["post_id"]
    title = request.form["title"]
    content = request.form["content"]
    author = request.form["author"]

    cursor = db.cursor()

    cursor.execute(
        """
        UPDATE blog_posts
        SET title=%s,
            content=%s,
            author=%s
        WHERE post_id=%s
        """,
        (title, content, author, post_id)
    )

    db.commit()

    cursor.close()

    return render_template("update_post_success.html")

@app.route("/deletepost")
def deletepost():
    return render_template("deletepost.html")

@app.route("/deletepostrecord", methods=["POST"])
def deletepostrecord():

    post_id = request.form["post_id"]

    cursor = db.cursor()

    cursor.execute(
        """
        DELETE FROM blog_posts
        WHERE post_id=%s
        """,
        (post_id,)
    )

    db.commit()

    cursor.close()

    return render_template("delete_post_success.html")

@app.route("/savecomment", methods=["POST"])
def savecomment():

    post_id = request.form["post_id"]
    username = request.form["username"]
    comment = request.form["comment"]

    cursor = db.cursor()

    cursor.execute(
        """
        INSERT INTO comments
        (post_id, username, comment)
        VALUES(%s, %s, %s)
        """,
        (post_id, username, comment)
    )

    db.commit()

    cursor.close()

    return redirect(f"/postdetails/{post_id}")


@app.route("/savereply", methods=["POST"])
def savereply():

    comment_id = request.form["comment_id"]
    post_id = request.form["post_id"]
    username = request.form["username"]
    reply = request.form["reply"]

    cursor = db.cursor()

    cursor.execute(
        """
        INSERT INTO replies
        (comment_id, username, reply)
        VALUES(%s,%s,%s)
        """,
        (comment_id, username, reply)
    )

    db.commit()

    cursor.close()

    return redirect(f"/postdetails/{post_id}")

if __name__ == "__main__":
    app.run(debug=True)