# ----------------------------------------
# models.py：レビュー用DBモデル定義
# 使用技術：Flask-SQLAlchemy
# ----------------------------------------

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


# DBインスタンス（Flask本体から分離）
db = SQLAlchemy()

# レビュー情報のテーブル定義
class Review(db.Model):
    __tablename__ = 'reviews'  # テーブル名

    id = db.Column(db.Integer, primary_key=True)  # ID（主キー）
    spot_name = db.Column(db.String(100), nullable=False)  # 観光地名
    comment = db.Column(db.Text, nullable=False)  # コメント
    rating = db.Column(db.Integer, nullable=False)  # 評価（1〜5）
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # レビュー投稿日時（自動で現在時刻を記録）


    def __repr__(self):
        return f'<Review {self.spot_name} - {self.rating}★>'