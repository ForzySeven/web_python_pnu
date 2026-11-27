from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, Regexp


class ContactForm(FlaskForm):
  name = StringField(
      "Name",
      validators=[
          DataRequired(message="Поле імені є обов'язковим."),
          Length(
              min=4,
              max=10,
              message="Ім'я повинно містити від 4 до 10 символів.",
          ),
      ],
  )
  email = StringField(
      "Email",
      validators=[
          DataRequired(message="Введіть email."),
          Email(message="Некоректний формат електронної пошти."),
      ],
  )
  phone = StringField(
      "Phone",
      validators=[
          DataRequired(message="Введіть номер телефону."),
          Regexp(
              r"^\+380\d{9}$",
              message="Формат номера має бути +380XXXXXXXXX (9 цифр після +380).",
          ),
      ],
  )
  subject = SelectField(
      "Subject",
      choices=[
          ("general", "Загальне питання"),
          ("support", "Технічна підтримка"),
          ("cooperation", "Співпраця / Замовлення"),
          ("feedback", "Відгук або пропозиція"),
      ],
      validators=[DataRequired()],
  )
  message = TextAreaField(
      "Message",
      validators=[
          DataRequired(message="Введіть текст повідомлення."),
          Length(
              max=500,
              message="Повідомлення не може перевищувати 500 символів.",
          ),
      ],
  )
  submit = SubmitField("Send Message")