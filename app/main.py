from flask import Flask, render_template
import os

app = Flask(__name__)


@app.route("/")
def home():
    version = os.getenv("APP_VERSION", "2.0")
    return render_template("index.html", version=version)


@app.route("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
