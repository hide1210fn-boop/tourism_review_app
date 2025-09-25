# ----------------------------------------
# forms.py：レビュー投稿フォームの定義
# 使用ライブラリ：Flask-WTF（WTForms）
# ----------------------------------------

from flask_wtf import FlaskForm  # Flask用のフォーム基底クラス
from wtforms import StringField, TextAreaField, IntegerField, SubmitField  # 入力欄の種類
from wtforms.validators import DataRequired, NumberRange  # 入力チェック用のルール

# 観光地レビュー投稿フォーム（名称・コメント・評価）
class ReviewForm(FlaskForm):
    # 観光地名（必須入力）
    spot_name = StringField('観光地名', validators=[DataRequired()])

    # コメント（必須入力）
    comment = TextAreaField('コメント', validators=[DataRequired()])

    # 評価（1〜5の整数、必須）
    rating = IntegerField('評価（1〜5）', validators=[
        DataRequired(),            # 入力必須
        NumberRange(min=1, max=5)  # 1〜5の範囲に限定
    ])

    # 投稿ボタン
    submit = SubmitField('投稿する')