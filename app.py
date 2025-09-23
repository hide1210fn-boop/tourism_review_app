from flask import Flask, render_template, redirect, url_for, request
from forms import ReviewForm
from models import db, Review  # 分離されたモデルとDBインスタンスをインポート
import os  # 追加：OSパス操作用

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # セキュリティキー（任意の文字列）

# プロジェクト直下の SQLite に変更
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'reviews.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 警告回避のため追加

db.init_app(app)  # FlaskアプリにDBを紐づけ

# 初回起動時にDBを作成（必要に応じて）
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    form = ReviewForm()

    if form.validate_on_submit():
        new_review = Review(
            spot_name=form.spot_name.data,
            comment=form.comment.data,
            rating=form.rating.data
        )
        db.session.add(new_review)
        db.session.commit()
        return redirect(url_for('index'))

    reviews = Review.query.all()
    return render_template('index.html', form=form, reviews=reviews)

@app.route('/review/<int:review_id>')
def review_detail(review_id):
    review = Review.query.get_or_404(review_id)
    return render_template('detail.html', review=review)

if __name__ == '__main__':
    app.run(debug=True)
