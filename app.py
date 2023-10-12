from flask import Flask, render_template, request, redirect, url_for
from peewee import Model, CharField, SqliteDatabase
from matching_algorithm import perform_matching, calculate_match_score


app = Flask(__name__)

# データベースの設定
db = SqliteDatabase('peewee_db.sqlite')
app.template_folder = "templates"


class Profile(Model):
    name = CharField()
    age = CharField()
    occupation = CharField()
    interests = CharField()
    means = CharField()
    book_title = CharField()
    topic_theme = CharField()

    class Meta:
        database = db

# テーブルが存在しない場合、作成する
db.connect()
db.create_tables([Profile], safe=True)
db.close()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit_profile", methods=["POST"])
def submit_profile():
    name = request.form["name"]
    age = request.form["age"]
    occupation = request.form["occupation"]
    interests = request.form["interests"]
    means = request.form["info_source"]
    book_title = request.form["book_title"]
    topic_theme = request.form["topic_theme"]

    # データベースにプロフィール情報を保存
    profile = Profile.create(
        name=name,
        age=age,
        occupation=occupation,
        interests=interests,
        means=means,
        book_title=book_title,
        topic_theme=topic_theme
    )

    # マッチングアルゴリズムを実行
    matches = perform_matching(profile)

    # マッチング結果を"Thank You"ページに渡してリダイレクト
    return redirect(url_for("thank_you", matches=matches, name=name, age=age, occupation=occupation, interests=interests, means=means, book_title=book_title, topic_theme=topic_theme))

@app.route("/thank_you")
def thank_you():
    matches = request.args.get("matches").split(',')
    name = request.args.get("name")
    age = request.args.get("age")
    occupation = request.args.get("occupation")
    interests = request.args.get("interests")
    means = request.args.get("means")
    book_title = request.args.get("book_title")
    topic_theme = request.args.get("topic_theme")

    return render_template("thank_you.html", matches=matches, name=name, age=age, occupation=occupation, interests=interests, means=means, book_title=book_title, topic_theme=topic_theme)


if __name__ == "__main__":
    app.run(port=8000, debug=True)
