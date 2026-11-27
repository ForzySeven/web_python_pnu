import os
import uuid
from flask import abort, flash, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename
from . import products_bp
from .db import create_product, delete_product_by_id, get_all_products, get_product_by_id, update_product
from .forms import ProductForm


def save_uploaded_image(file_storage):
  """Безпечно зберігає зображення з унікальним UUID-іменем у static/uploads/."""
  if not file_storage or not file_storage.filename:
    return ""

  original_name = secure_filename(file_storage.filename)
  ext = os.path.splitext(original_name)[1].lower()
  unique_filename = f"{uuid.uuid4().hex}{ext}"

  upload_dir = os.path.join(products_bp.static_folder, "uploads")
  os.makedirs(upload_dir, exist_ok=True)

  file_path = os.path.join(upload_dir, unique_filename)
  file_storage.save(file_path)

  # Зберігаємо відносний шлях відносно static блюпринта
  return f"uploads/{unique_filename}"


@products_bp.route("/")
def product_list():
  items = get_all_products()
  return render_template("products.html", products=items)


@products_bp.route("/add", methods=["GET", "POST"])
def add_product():
  form = ProductForm()
  if form.validate_on_submit():
    image_rel_path = save_uploaded_image(form.image.data)
    create_product(
        name=form.name.data,
        content=form.content.data,
        price=form.price.data,
        category=form.category.data,
        quantity=form.quantity.data,
        image=image_rel_path,
    )
    flash("Товар успішно додано!", "success")
    return redirect(url_for("products.product_list"))

  return render_template(
      "product_form.html", form=form, form_title="Додати новий товар"
  )


@products_bp.route("/<int:id>")
def detail_product(id):
  product = get_product_by_id(id)
  if product is None:
    abort(404)
  return render_template("detail_product.html", product=product)


@products_bp.route("/<int:id>/edit", methods=["GET", "POST"])
def edit_product(id):
  product = get_product_by_id(id)
  if product is None:
    abort(404)

  form = ProductForm()
  if form.validate_on_submit():
    # Якщо завантажено новий файл — оновлюємо, інакше залишаємо старий шлях
    if form.image.data and form.image.data.filename:
      image_rel_path = save_uploaded_image(form.image.data)
    else:
      image_rel_path = product.get("image", "")

    update_product(
        product_id=id,
        name=form.name.data,
        content=form.content.data,
        price=form.price.data,
        category=form.category.data,
        quantity=form.quantity.data,
        image=image_rel_path,
    )
    flash("Зміни товару успішно збережено!", "success")
    return redirect(url_for("products.detail_product", id=id))

  if request.method == "GET":
    form.name.data = product["name"]
    form.content.data = product["content"]
    form.price.data = product["price"]
    form.category.data = product["category"]
    form.quantity.data = product["quantity"]

  return render_template(
      "product_form.html",
      form=form,
      form_title=f"Редагування: {product['name']}",
      product=product,
  )


@products_bp.route("/<int:id>/delete", methods=["POST"])
def delete_product(id):
  product = get_product_by_id(id)
  if product is None:
    abort(404)

  delete_product_by_id(id)
  flash(f"Товар '{product['name']}' видалено.", "info")
  return redirect(url_for("products.product_list"))