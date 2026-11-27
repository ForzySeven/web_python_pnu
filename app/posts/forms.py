from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import BooleanField, DateTimeLocalField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional


class PostForm(FlaskForm):
  title = StringField(
      "Заголовок",
      validators=[
          DataRequired(message="Введіть заголовок поста."),
          Length(max=150, message="Максимум 150 символів."),
      ],
  )
  content = TextAreaField(
      "Текст публікації",
      render_kw={"rows": 6},
      validators=[DataRequired(message="Введіть текст поста.")],
  )
  enabled = BooleanField("Активний (відображати на сайті)", default=True)
  publish_date = DateTimeLocalField(
      "Дата публікації",
      format="%Y-%m-%dT%H:%M",
      default=datetime.now,
      validators=[Optional()],
  )
  category = SelectField(
      "Категорія",
      choices=[
          ("news", "Новина (News)"),
          ("publication", "Публікація (Publication)"),
          ("tech", "Технології (Tech)"),
          ("other", "Інше (Other)"),
      ],
      validators=[DataRequired()],
  )
  submit = SubmitField("Зберегти пост")