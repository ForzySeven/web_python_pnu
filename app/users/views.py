from flask import flash, make_response, redirect, render_template, request, session, url_for
from . import user_bp

# Заглушка облікових даних без використання бази даних
USERS_DB = {
    "user1": "1234",
    "admin": "admin",
}


@user_bp.route("/hi/<string:name>")
def greetings(name):
  name = name.upper()
  age = request.args.get("age", None, int)
  return render_template("hi.html", name=name, age=age)


@user_bp.route("/admin")
def admin():
  to_url = url_for(
      "users.greetings", name="administrator", age=45, _external=True
  )
  return redirect(to_url)


# --- Завдання 1: Вхід, Профіль, Вихід ---


@user_bp.route("/login", methods=["GET", "POST"])
def login():
  if request.method == "POST":
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "").strip()

    if username in USERS_DB and USERS_DB[username] == password:
      session["username"] = username
      flash(f"Вітаємо, {username}! Ви успішно увійшли в систему.", "success")
      return redirect(url_for("users.profile"))
    else:
      flash("Wrong data! Try again!", "danger")
      return redirect(url_for("users.login"))

  return render_template("login.html")


@user_bp.route("/profile")
def profile():
  if "username" not in session:
    flash(
        "Будь ласка, увійдіть у систему для доступу до профілю.",
        "danger",
    )
    return redirect(url_for("users.login"))

  username = session["username"]
  cookies = request.cookies
  theme = request.cookies.get("theme", "light")

  return render_template(
      "profile.html",
      username=username,
      cookies=cookies,
      theme=theme,
  )


@user_bp.route("/logout", methods=["GET", "POST"])
def logout():
  session.pop("username", None)
  flash("Ви успішно вийшли із системи.", "info")
  return redirect(url_for("users.login"))


# --- Завдання 2: Керування кукі ---


@user_bp.route("/cookie/add", methods=["POST"])
def add_cookie():
  if "username" not in session:
    flash("Доступ заборонено. Увійдіть у систему.", "danger")
    return redirect(url_for("users.login"))

  key = request.form.get("cookie_key", "").strip()
  value = request.form.get("cookie_value", "").strip()
  max_age_raw = request.form.get("cookie_max_age", "").strip()

  if not key or not value:
    flash("Вкажіть ключ та значення кукі!", "warning")
    return redirect(url_for("users.profile"))

  max_age = int(max_age_raw) if max_age_raw.isdigit() else None

  response = make_response(redirect(url_for("users.profile")))
  response.set_cookie(key, value, max_age=max_age)
  flash(f"Кукі '{key}' успішно додано!", "success")
  return response


@user_bp.route("/cookie/delete", methods=["POST"])
def delete_cookie():
  if "username" not in session:
    flash("Доступ заборонено. Увійдіть у систему.", "danger")
    return redirect(url_for("users.login"))

  key = request.form.get("delete_key", "").strip()
  response = make_response(redirect(url_for("users.profile")))

  if key in request.cookies and key != "session":
    response.delete_cookie(key)
    flash(f"Кукі '{key}' успішно видалено!", "success")
  else:
    flash(
        f"Кукі з ключем '{key}' не знайдено або його не можна видалити.",
        "warning",
    )

  return response


@user_bp.route("/cookie/delete_all", methods=["POST"])
def delete_all_cookies():
  if "username" not in session:
    flash("Доступ заборонено. Увійдіть у систему.", "danger")
    return redirect(url_for("users.login"))

  response = make_response(redirect(url_for("users.profile")))
  # Видаляємо всі користувацькі кукі, зберігаючи технічну кукі 'session', щоб не викинути користувача з акаунта
  for key in request.cookies:
    if key != "session":
      response.delete_cookie(key)

  flash("Усі збережені кукі успішно видалено!", "success")
  return response


# --- Завдання 3: Вибір кольорової схеми ---


@user_bp.route("/theme/<string:scheme>")
def set_theme(scheme):
  if "username" not in session:
    flash("Увійдіть у систему для зміни теми.", "danger")
    return redirect(url_for("users.login"))

  if scheme not in ("light", "dark"):
    scheme = "light"

  response = make_response(redirect(url_for("users.profile")))
  # Зберігаємо вибір теми у кукі на 30 днів, щоб він діяв при наступних відвідуваннях
  response.set_cookie("theme", scheme, max_age=30 * 24 * 60 * 60)
  flash(
      f"Кольорову схему змінено на {'темну' if scheme == 'dark' else 'світлу'}.",
      "info",
  )
  return response