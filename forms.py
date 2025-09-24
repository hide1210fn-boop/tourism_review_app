# Flask-WTF を使ってフォームを定義するための基底クラスをインポート
from flask_wtf import FlaskForm

# フォームで使用する各種フィールドとバリデーションをインポート
from wtforms import StringField, TextAreaField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange

# 観光スポットのレビュー投稿フォームの定義
class ReviewForm(FlaskForm):
    # 観光地名の入力欄（空欄禁止）
    spot_name = StringField('観光地名', validators=[DataRequired()])

    # コメントの入力欄（空欄禁止）
    comment = TextAreaField('コメント', validators=[DataRequired()])

    # 評価（1〜5の整数）を入力する欄（空欄禁止＋範囲指定）
    rating = IntegerField('評価（1〜5）', validators=[
        DataRequired(),              # 入力必須
        NumberRange(min=1, max=5)    # 1〜5の範囲に限定
    ])

    submit = SubmitField('投稿する')