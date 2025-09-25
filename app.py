# -----------------------------------------------
# Flaskアプリケーション：観光地レビュー投稿・閲覧システム
# - トップページでレビュー投稿と一覧表示
# - 詳細ページで個別レビューの表示
# - SQLiteとSQLAlchemyによるデータ管理
# -----------------------------------------------

from flask import Flask, render_template, redirect, url_for, request
from forms import ReviewForm  # WTFormsで定義したレビュー投稿フォーム
from models import db, Review  # SQLAlchemyによるDBモデルとインスタンス
import os  # DBファイルのパス指定に使用

# Flaskアプリケーションの初期化
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # CSRF対策などに使用

# SQLiteデータベースのパスをプロジェクト直下に設定
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'reviews.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # モデル変更の追跡を無効化（警告抑制）

# DBの初期化とテーブル作成（アプリケーションコンテキスト内で実行）
db.init_app(app)
with app.app_context():
    db.create_all()  # 初回起動時にテーブル作成

# -----------------------------------------------
# トップページ：レビュー投稿フォームとレビュー一覧表示
# -----------------------------------------------
@app.route('/', methods=['GET', 'POST'])
def index():
    form = ReviewForm()  # 投稿フォームの生成

    if form.validate_on_submit():  # フォーム送信時の処理（バリデーション成功時）
        new_review = Review(
            spot_name=form.spot_name.data,
            comment=form.comment.data,
            rating=form.rating.data
        )
        db.session.add(new_review)  # 新規レビューをDBに追加
        db.session.commit()         # DBへ保存
        return redirect(url_for('index'))  # 投稿後はトップページにリダイレクト

    reviews = Review.query.all()  # 登録済みレビューを全件取得
    return render_template('index.html', form=form, reviews=reviews)  # テンプレートに渡して表示

# -----------------------------------------------
# 詳細ページ：指定IDのレビューを個別表示
# -----------------------------------------------
@app.route('/review/<int:review_id>')
def review_detail(review_id):
    review = Review.query.get_or_404(review_id)  # 該当レビューがなければ404エラー
    return render_template('detail.html', review=review)  # テンプレートに渡して表示

# -----------------------------------------------
# アプリケーションの起動（デバッグモード）
# -----------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
