# ------------------------------------------------------------
# アプリ名 : 観光レビュー投稿アプリ（Flask）
# 概要     : 観光スポットのレビュー（名称・コメント・評価）を投稿・閲覧
# 技術     : Flask / SQLAlchemy / WTForms / SQLite
# URL      : "/"（投稿＋一覧）, "/review/<id>"（詳細表示）
# 実行     : python app.py（開発時は debug=True）
# 注意     : SECRET_KEY は本番環境で安全に管理 / DBは reviews.db（SQLite）
# ------------------------------------------------------------

from flask import Flask, render_template, redirect, url_for, request
from forms import ReviewForm  # WTFormsで定義したレビュー投稿フォーム
from models import db, Review  # SQLAlchemyによるDBモデルとインスタンス
import os  # DBファイルのパス指定に使用

# ------------------------------
# Flaskアプリの初期設定
# ------------------------------
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # セッション管理・CSRF対策用（本番では環境変数推奨）

# ------------------------------
# SQLiteデータベースの設定
# - プロジェクト直下に reviews.db を作成
# ------------------------------
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'reviews.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # モデル変更の追跡を無効化（警告抑制）

# ------------------------------
# DB初期化とテーブル作成
# - FlaskアプリにDBを紐づけ
# - アプリケーションコンテキスト内で create_all() 実行
# ------------------------------
db.init_app(app)
with app.app_context():
    db.create_all()

# ------------------------------
# ルート "/"：レビュー投稿と一覧表示（GET/POST）
# ------------------------------
@app.route('/', methods=['GET', 'POST'])
def index():
    form = ReviewForm()  # 投稿フォームの生成

    # フォーム送信時（POST）かつバリデーション成功時の処理
    if form.validate_on_submit():
        new_review = Review(
            spot_name=form.spot_name.data,
            comment=form.comment.data,
            rating=form.rating.data
        )
        db.session.add(new_review)  # 新規レビューをDBに追加
        db.session.commit()         # DBへ保存
        return redirect(url_for('index'))  # 投稿後はトップページにリダイレクト（PRGパターン）

    # GET時またはバリデーション失敗時：レビュー一覧を取得して表示
    reviews = Review.query.all()
    return render_template('index.html', form=form, reviews=reviews)

# ------------------------------
# ルート "/review/<int:review_id>"：レビュー詳細表示（GET）
# ------------------------------
@app.route('/review/<int:review_id>')
def review_detail(review_id):
    review = Review.query.get_or_404(review_id)  # 該当レビューがなければ404エラー
    return render_template('detail.html', review=review)

# ------------------------------
# アプリケーションの起動（開発用）
# ------------------------------
if __name__ == '__main__':
    app.run(debug=True)