from datetime import datetime, timezone
from flask import flash, redirect, render_template, request, session, url_for
from app import db
from . import post_bp
from .forms import PostForm
from .models import Post


@post_bp.route("/")
def all_posts():
  stmt = (
      db.select(Post)
      .where(Post.is_active == True)
      .order_by(Post.posted.desc())
  )
  posts = db.session.scalars(stmt).all()
  return render_template("posts.html", posts=posts)


@post_bp.route("/create", methods=["GET", "POST"])
def create_post():
  form = PostForm()
  if form.validate_on_submit():
    author_name = session.get("username", "Anonymous")
    posted_dt = form.publish_date.data or datetime.now(timezone.utc)

    new_post = Post(
        title=form.title.data,
        content=form.content.data,
        is_active=form.enabled.data,
        posted=posted_dt,
        category=form.category.data,
        author=author_name,
    )
    db.session.add(new_post)
    db.session.commit()
    flash("Post added successfully", "success")
    return redirect(url_for("posts.all_posts"))

  return render_template(
      "add_post.html", form=form, form_title="Створити новий пост"
  )


@post_bp.route("/<int:id>")
def detail_post(id):
  post = db.get_or_404(Post, id)
  return render_template("detail_post.html", post=post)


@post_bp.route("/<int:id>/update", methods=["GET", "POST"])
def update_post(id):
  post = db.get_or_404(Post, id)
  form = PostForm(obj=post)

  if request.method == "GET":
    form.enabled.data = post.is_active
    form.publish_date.data = post.posted

  if form.validate_on_submit():
    form.populate_obj(post)
    post.is_active = form.enabled.data
    if form.publish_date.data:
      post.posted = form.publish_date.data

    db.session.commit()
    flash("Post updated successfully", "success")
    return redirect(url_for("posts.detail_post", id=post.id))

  return render_template(
      "add_post.html", form=form, form_title="Редагувати пост", post=post
  )


@post_bp.route("/<int:id>/delete", methods=["GET", "POST"])
def delete_post(id):
  post = db.get_or_404(Post, id)

  if request.method == "POST":
    db.session.delete(post)
    db.session.commit()
    flash("Post deleted successfully", "info")
    return redirect(url_for("posts.all_posts"))

  return render_template("delete_confirm.html", post=post)