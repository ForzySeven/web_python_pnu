from datetime import datetime
import os
from tinydb import Query, TinyDB

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

DB_PATH = os.path.join(DATA_DIR, "products.json")


def get_table():
  db = TinyDB(DB_PATH, ensure_ascii=False, indent=4)
  return db.table("products")


def get_all_products():
  return get_table().all()


def get_product_by_id(product_id):
  Product = Query()
  return get_table().get(Product.id == product_id)


def create_product(name, content, price, category, quantity, image=""):
  table = get_table()
  all_items = table.all()
  next_id = max([item.get("id", 0) for item in all_items], default=0) + 1

  product_data = {
      "id": next_id,
      "name": name,
      "content": content,
      "price": round(float(price), 2),
      "category": category,
      "quantity": int(quantity),
      "image": image,
      "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
  }
  table.insert(product_data)
  return product_data


def update_product(product_id, name, content, price, category, quantity, image):
  Product = Query()
  table = get_table()
  table.update(
      {
          "name": name,
          "content": content,
          "price": round(float(price), 2),
          "category": category,
          "quantity": int(quantity),
          "image": image,
      },
      Product.id == product_id,
  )


def delete_product_by_id(product_id):
  Product = Query()
  get_table().remove(Product.id == product_id)