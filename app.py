from flask import (
    Flask,
    render_template,
    url_for,
    request,
    session,
    redirect,
    sessions,
    send_from_directory,
)
from flask_login import LoginManager
import bcrypt
import pymongo.errors
from database.mongodbusers import users
from database.mongodbposts import posts
from database.mongocomments import comments
import pymongo
from gen_utility.email_auth import verify_email
from gen_utility.markdown_conv import convert_md
from datetime import date
import os
from dotenv import load_dotenv
import dns
from bson.objectid import ObjectId

load_dotenv()

# Secret Key
secret_key = os.getenv("SECRET_KEY")


# Init flask app
app = Flask(__name__)
app.secret_key = secret_key


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


@app.route("/admin", methods=["POST", "GET"])
def admin():
    try:
        if session["user"] == "syedabimam@gmail.com":
            post_list = posts.find()
            comment_list = comments.find()
            user_count = users.count_documents({})

            if request.method == "POST":
                title = request.form["title"]
                description = request.form["description"]
                body = request.form["body"]

                post = {
                    "title": title,
                    "description": description,
                    "author": "Malanaa",
                    "time": str(date.today()),
                    "body": body,
                }

                posts.insert_one(post)

                return redirect(url_for("admin", message="Succesfuly Posted"))
            return render_template(
                "admin.html",
                posts=post_list,
                comments=comment_list,
                user_count=user_count,
            )

            # return render_template("admin.html")
        return redirect(url_for("home"))
    except KeyError:
        return redirect(url_for("home"))


@app.route("/comment", methods=["POST", "GET"])
def comment():
    title = request.args.get("title")
    user = request.args.get("user")
    user = user.split("@")[0]

    if request.method == "POST":
        comment = request.form["comment"]
        blog = posts.find_one({"title": f"{title}"})
        blog_id = blog.get("_id")

        comment = {
            "user": user,
            "blog": blog_id,
            "comment": comment,
            "time": str(date.today()),
        }

        comments.insert_one(comment)

        return redirect(url_for("blogpost", title=title))

    return redirect(url_for("blogpost", title=title))


@app.route("/<title>")
def blogpost(title):
    title_real = title.replace("-", " ")
    try:
        if session["logged_in"] == True:
            user = session["user"]
            post_current = posts.find_one({"title": f"{title_real}"})

            if post_current:
                description = post_current.get("description")
                time = post_current.get("time")
                body = post_current.get("body")
                body = convert_md(body)

                comment_list = comments.find({"blog": post_current.get("_id")}).sort(
                    "_id", -1
                )

                if comment_list:
                    return render_template(
                        "blogpost.html",
                        title=title_real,
                        description=description,
                        time=time,
                        body=body,
                        user=user,
                        comments=comment_list,
                    )

                return render_template(
                    "blogpost.html",
                    title=title_real,
                    description=description,
                    time=time,
                    body=body,
                    user=user,
                )
        return render_template("blogpost.html")
    except KeyError:
        post_current = posts.find_one({"title": f"{title_real}"})
        if post_current:
            description = post_current.get("description")
            time = post_current.get("time")
            body = post_current.get("body")
            body = convert_md(body)

            comment_list = comments.find({"blog": post_current.get("_id")}).sort(
                "_id", -1
            )

            if comment_list:
                return render_template(
                    "blogpost.html",
                    title=title_real,
                    description=description,
                    time=time,
                    body=body,
                    comments=comment_list,
                )

            return render_template(
                "blogpost.html",
                title=title_real,
                description=description,
                time=time,
                body=body,
            )
        return render_template("blogpost.html")


@app.route("/blog")
def blog():
    title = request.args.get("title")
    title_url = title.replace(" ", "-")
    return redirect(url_for("blogpost", title=title_url))


@app.route("/search", methods=["POST", "GET"])
def search():
    search_word = request.form.get("search")
    post_list = posts.find({"title": {"$regex": search_word, "$options": "i"}})
    try:
        if session["logged_in"] == True:
            user = session["user"]
            return render_template("home.html", user=user, posts=post_list)
        return render_template("home.html", posts=post_list)
    except KeyError:
        return render_template("home.html", posts=post_list)


@app.route("/", methods=["POST", "GET"])
@app.route("/home", methods=["POST", "GET"])
def home():
    posts_list = posts.find().sort("_id", -1)

    try:
        if session["logged_in"] == True:

            user = session["user"]

            if session["user"] == "syedabimam@gmail.com":
                user = session["user"]
                return render_template(
                    "home.html", user=user, admin=True, posts=posts_list
                )

            return render_template("home.html", user=user, posts=posts_list)

        return render_template("home.html", posts=posts_list)
    except KeyError:
        return render_template("home.html", posts=posts_list)


@app.route("/auth", methods=["POST", "GET"])
def auth():
    if request.method == "POST":
        if request.form["email"] and request.form["password"]:

            email = request.form["email"]
            password = request.form["password"]

            if verify_email(email=email):

                b_password = password.encode("utf-8")
                salt = bcrypt.gensalt()
                hashed_password = bcrypt.hashpw(b_password, salt=salt)

                user_now = {
                    "email": email,
                    "password_hash": hashed_password,
                }

                try:
                    users.insert_one(user_now)
                    session["logged_in"] = True
                    session["user"] = email
                    return redirect(url_for("home"))
                except pymongo.errors.DuplicateKeyError:
                    find_email = users.find_one({"email": f"{email}"})
                    if find_email:
                        find_password_hash = find_email.get("password_hash")
                        password = bytes(password, "utf-8")
                        if bcrypt.checkpw(
                            password=password, hashed_password=find_password_hash
                        ):
                            session["logged_in"] = True
                            session["user"] = email
                            return redirect(url_for("home"))
                        else:
                            return render_template(
                                "auth.html",
                                message="Invalid Password / Email Already Taken",
                            )
            else:
                return render_template("auth.html", message="Invalid Email")
        else:
            return render_template("auth.html", error=True)
    return render_template("auth.html")


@app.route("/XPIysYkz9L")
def delete():
    post_id = request.args.get("post_id")
    deleted_comment = comments.delete_many({"blog": ObjectId(post_id)})
    deleted_result = posts.delete_one({"_id": ObjectId(post_id)})
    return redirect(url_for("admin"))


@app.route("/XPIysYkAAssQ!z9L")
def delete_comment():
    comment_id = request.args.get("comment_id")
    deleted_comment = comments.delete_many({"_id": ObjectId(comment_id)})
    return redirect(url_for("admin"))


@app.route("/sitemap.xml")
@app.route("/sitemap.xml")
def sitemap():
    return send_from_directory("static", "sitemap.xml")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
