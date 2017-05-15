from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/auth")
def auth():
    return render_template("bleh.html")

@app.route("/form")#gonna change
def form():
    return render_template("stuff.html")


if (__name__ == '__main__'):
    app.debug = True

app.run()
