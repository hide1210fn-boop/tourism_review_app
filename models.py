from flask_sqlalchemy import SQLAlchemy

# SQLAlchemyインスタンスを定義（アプリ本体から分離）
db = SQLAlchemy()

# レビューのテーブル定義
class Review(db.Model):
    __tablename__ = 'reviews'  # テーブル名を明示

    id = db.Column(db.Integer, primary_key=True)
    spot_name = db.Column(db.String(100), nullable=False)
    comment = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1〜5の整数を想定

    def __repr__(self):
        return f'<Review {self.spot_name} - {self.rating}★>'