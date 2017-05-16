from flask import Flask, render_template #session stuff

app = Flask(__name__)

@app.route("/", methods =['GET', 'POST'])
def index():
    return render_template("login.html", msg = "Please login to your account.")

@app.route("/auth")
def auth():
    username = request.form["user"]
    password = request.form["pw"]
    if user == "" or password == "":
        return render_template("login.html", msg="Please enter your username and password.")
    if ():#username not in database
        return render_template("login.html", msg = "Username incorrect. Please try again.")
    if ():#username right, password wrong
        return render_template("login.html", msg = "Password incorrect. Please try again.")
    return redirect("/form")

@app.route("/form")
def form():
    return render_template("form.html")


if __name__ == '__main__':
    app.debug = True
    app.run()
