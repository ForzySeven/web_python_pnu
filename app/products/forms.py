from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import DecimalField, IntegerField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, NumberRange


class ProductForm(FlaskForm):
  name = StringField(
      "Назва товару",
      validators=[
          DataRequired(message="Вкажіть назву товару."),
          Length(
              min=3, message="Назва повинна містити щонайменше 3 символи."
          ),
      ],
  )
  content = TextAreaField(
      "Опис товару",
      render_kw={"rows": 5, "cols": 40},
      validators=[DataRequired(message="Додайте опис товару.")],
  )
  price = DecimalField(
      "Ціна ($)",
      places=2,
      validators=[
          DataRequired(message="Вкажіть ціну."),
          NumberRange(min=0.01, message="Ціна повинна бути додатним числом."),
      ],
  )
  category = SelectField(
      "Категорія",
      choices=[
          ("Laptops", "Ноутбуки"),
          ("Smartphones", "Смартфони"),
          ("PC", "Настільні ПК"),
          ("Accessories", "Аксесуари"),
      ],
      validators=[DataRequired()],
  )
  quantity = IntegerField(
      "Кількість одиниць",
      validators=[
          DataRequired(message="Вкажіть кількість."),
          NumberRange(
              min=0, message="Кількість не може бути від'ємним числом."
          ),
      ],
  )
  image = FileField(
      "Зображення товару (PNG, JPG, JPEG)",
      validators=[
          FileAllowed(
              ["png", "jpg", "jpeg"],
              "Дозволені лише зображення у форматах PNG, JPG або JPEG!",
          )
      ],
  )
  submit = SubmitField("Зберегти товар")