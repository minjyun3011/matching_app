from flask import Flask, render_template, request, redirect, url_for
from peewee import Model, CharField, SqliteDatabase
from matching_algorithm import perform_matching


app = Flask(__name__)

# データベースの設定
db = SqliteDatabase("peewee_db.sqlite")
app.template_folder = "templates"


class Profile(Model):
    name = CharField()
    age = CharField()
    occupation = CharField()
    info_source = CharField()
    type_of_communication = CharField()
    talk_contents_title = CharField()
    your_objection = CharField()
    other_topic_theme = CharField()

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
    info_source = request.form["info_source"]
    type_of_communication = request.form["type_of_communication"]
    talk_contents_title = request.form["talk_contents_title"]
    your_objection = request.form["your_objection"]
    other_topic_theme = request.form["other_topic_theme"]

    # データベースにプロフィール情報を保存
    profile = Profile.create(
        name=name,
        age=age,
        occupation=occupation,
        info_source=info_source,
        type_of_communication=type_of_communication,
        talk_contents_title=talk_contents_title,
        your_objection=your_objection,
        other_topic_theme=other_topic_theme,
    )

    # マッチングアルゴリズムを実行
    matches = perform_matching(profile)

    # マッチング結果を"Thank You"ページに渡してリダイレクト
    return redirect(
        url_for(
            "thank_you",
            matches=matches,
            name=name,
            age=age,
            occupation=occupation,
            info_source=info_source,
            type_of_communication=type_of_communication,
            talk_contents_title=talk_contents_title,
            your_objection=your_objection,
            other_topic_theme=other_topic_theme,
        )
    )


@app.route("/thank_you")
def thank_you():
    matches = request.args.get("matches").split(",")
    name = request.args.get("name")
    age = request.args.get("age")
    occupation = request.args.get("occupation")
    info_source = request.args.get("info_source")
    type_of_communication = request.args.get("type_of_communication")
    talk_contents_title = request.args.get("talk_contents_title")
    your_objection = request.args.get("your_objection")
    other_topic_theme = request.args.get("other_topic_theme")

    return render_template(
        "matching.html",
        matches=matches,
        name=name,
        age=age,
        occupation=occupation,
        info_source=info_source,
        type_of_communication=type_of_communication,
        talk_contents_title=talk_contents_title,
        your_objection=your_objection,
        other_topic_theme=other_topic_theme,
    )


if __name__ == "__main__":
    app.run(port=8000, debug=True)
