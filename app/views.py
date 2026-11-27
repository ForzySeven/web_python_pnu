import logging
from flask import flash, redirect, render_template, request, url_for
from . import app
from .forms import ContactForm

# Налаштування логування повідомлень з форми у файл
contact_logger = logging.getLogger("contact_form")
contact_logger.setLevel(logging.INFO)
if not contact_logger.handlers:
  file_handler = logging.FileHandler("contact_messages.log", encoding="utf-8")
  formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
  file_handler.setFormatter(formatter)
  contact_logger.addHandler(file_handler)


@app.route("/")
@app.route("/resume")
def resume():
  return render_template("resume.html", title="Резюме")


@app.route("/homepage")
def home():
  agent = request.user_agent
  return render_template("homepage.html", title="Головна", agent=agent)


@app.route("/contact", methods=["GET", "POST"])
@app.route("/contacts", methods=["GET", "POST"])
def contact():
  form = ContactForm()
  if form.validate_on_submit():
    log_msg = (
        f"Name: {form.name.data} | Email: {form.email.data} | "
        f"Phone: {form.phone.data} | Subject: {form.subject.data} | "
        f"Message: {form.message.data}"
    )
    contact_logger.info(log_msg)
    flash(
        "Повідомлення успішно відправлено та записано у лог-файл!", "success"
    )
    return redirect(url_for("contact"))

  if request.method == "POST":
    flash("Помилка валідації! Перевірте правильність заповнення полів.", "danger")

  return render_template("contacts.html", title="Контакти", form=form)