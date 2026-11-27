from flask import render_template
from . import post_bp


@post_bp.route("/")
def all_posts():
  return render_template("posts.html", posts=[])