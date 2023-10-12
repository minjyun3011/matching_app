from flask import Flask, request

app = Flask(__name__)


# ログイン機能
@app.route("/login", methods=["GET", "POST"])
def login():
    print(request.method)
    return "login page"

@app.route("/")
def home():
    return "Welcome to the homepage"


if __name__ == '__main__':
    app.run(port=8000, debug=True)