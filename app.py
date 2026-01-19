from flask import Flask, render_template
import verovio

app = Flask(__name__)
tk = verovio.toolkit()

@app.route("/scales")
def scale_page():
    return render_template("scale_page.html")

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run()
