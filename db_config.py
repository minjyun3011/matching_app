import os
import logging
from playhouse.db_url import connect
from dotenv import load_dotenv
from peewee import Model, CharField

# .envの読み込み
load_dotenv()

# ①実行したSQLをログで出力する設定
logger = logging.getLogger("peewee")
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

# データベースへの接続設定
# 環境変数からデータベースのURLを取得
database_url = os.environ.get("DATABASE")

# データベースに接続
db = connect(database_url)

# 接続NGの場合はメッセージを表示
if not db.connect():
    print("接続NG")
    exit()


# ③プロフィールのモデル
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


# データベースのテーブルを作成
db.create_tables([Profile])